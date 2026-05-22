"""Path safety checker for Aspose MCP plugin code.

Scans plugin source code for path handling violations that would cause
file access failures in hosted MCP environments (e.g. Claude Desktop on Windows).
"""

from __future__ import annotations

import ast
import re

# Patterns that indicate unsafe path usage
_BANNED_PATTERNS: list[tuple[str, str]] = [
    # os.getcwd() anywhere
    (r"\bos\.getcwd\s*\(\s*\)", "os.getcwd() is banned — use Path parameters instead"),
    # print() is checked via AST above (lines 83-92) to avoid false-positives on docstrings.
    # Do NOT add a regex entry for print() here.
    # Module-level aspose imports (top-level, not inside a function)
    # Detected via AST, but also check with regex as a belt-and-suspenders
    (r"^import aspose\b", "module-level 'import aspose' is banned — use lazy imports inside each tool function"),
    (r"^from aspose\b", "module-level 'from aspose' is banned — use lazy imports inside each tool function"),
    # open() with a bare relative string
    (r'(?<!\.)\bopen\s*\(\s*["\'][^/~][^"\']*["\']', "open() with a relative path string is banned — resolve to absolute first"),
    # Relative path literals used directly
    (r'(?<![/~\w])["\']\./', "relative path literal './' is banned — use Path().resolve()"),
    # Raw Path(param).resolve() without going through get_safe_path()
    # get_safe_path() handles stdio vs. network mode and prevents path traversal;
    # bare .resolve() silently converts "/tmp/x" to "C:\\tmp\\x" on Windows.
    # Exclude variables named resolved_* (already validated earlier in the same fn).
    (
        r"\bPath\s*\((?!resolved_)[a-z_]+\)\s*\.resolve\s*\(\s*\)",
        "bare Path(param).resolve() is banned — use get_safe_path(param) from "
        "mcp_server.path_utils for cross-platform safe path resolution",
    ),
]

# Patterns that should appear for path parameters (absence is a warning, not always caught here)
_RELATIVE_LITERAL_PATTERN = re.compile(
    r'(?:Path|open)\s*\(\s*["\'](?!(?:/|~|[A-Za-z]:\\|[A-Za-z]:/))([^"\']+)["\']'
)


def check_path_safety(code: str) -> list[str]:
    """Scan plugin code for path safety violations.

    Args:
        code: Python source code string to analyse.

    Returns:
        List of violation description strings. Empty list means all clear.

    Example:
        >>> violations = check_path_safety(open("ocr_plugin.py").read())
        >>> assert violations == [], f"Path safety violations: {violations}"
    """
    violations: list[str] = []

    # --- AST-based checks ---
    try:
        tree = ast.parse(code)
    except SyntaxError as exc:
        violations.append(f"Syntax error prevents path safety analysis: {exc}")
        return violations

    # Collect all function definition line numbers to detect module-level imports
    function_lines: set[int] = set()
    _collect_function_lines(tree, function_lines)

    for node in ast.walk(tree):
        # Check for os.getcwd()
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and node.func.attr == "getcwd"
            and isinstance(node.func.value, ast.Name)
            and node.func.value.id == "os"
        ):
            violations.append(
                f"Line {node.lineno}: os.getcwd() is banned — CWD is unpredictable "
                "in hosted environments. Use explicit path parameters."
            )

        # Check for print() calls
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "print"
        ):
            violations.append(
                f"Line {node.lineno}: print() is banned — "
                "use logging.getLogger(__name__) instead."
            )

        # Check for module-level aspose imports
        if isinstance(node, (ast.Import, ast.ImportFrom)) and not _is_inside_function(
            node, tree
        ):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name.startswith("aspose"):
                        violations.append(
                            f"Line {node.lineno}: module-level 'import {alias.name}' is banned. "
                            "Import aspose.* inside each tool function (lazy import)."
                        )
            elif isinstance(node, ast.ImportFrom) and node.module and node.module.startswith("aspose"):
                violations.append(
                    f"Line {node.lineno}: module-level 'from {node.module} import ...' is banned. "
                    "Import aspose.* inside each tool function (lazy import)."
                )

        # Check for relative path string literals passed to Path() or open()
        if isinstance(node, ast.Call):
            func_name = _get_call_name(node)
            if func_name in ("Path", "open"):
                # For open(), only flag top-level builtin calls (func is a Name node).
                # Skip method calls like path_obj.open("rb") — those are Path.open(),
                # not builtins.open(), and the first arg is a mode string, not a path.
                if func_name == "open" and not isinstance(node.func, ast.Name):
                    continue
                # For open(), only the first argument is a path; subsequent args are
                # mode/encoding/etc. and must not be flagged as relative paths.
                check_args = node.args[:1] if func_name == "open" else node.args
                for arg in check_args:
                    if isinstance(arg, ast.Constant) and isinstance(arg.value, str):
                        val = arg.value
                        # Relative if it doesn't start with /, ~, or a Windows drive letter
                        if val and not (
                            val.startswith("/")
                            or val.startswith("~")
                            or (len(val) >= 2 and val[1] == ":")
                        ):
                            violations.append(
                                f"Line {node.lineno}: {func_name}({val!r}) uses a relative path literal. "
                                "Use an absolute path or Path(param).resolve()."
                            )

        # Check for Path(var).resolve() — should use resolve_path(var) instead.
        # bare .resolve() silently converts Unix paths to broken Windows paths.
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and node.func.attr == "resolve"
            and isinstance(node.func.value, ast.Call)
            and _get_call_name(node.func.value) == "Path"
        ):
            inner_args = node.func.value.args
            if inner_args and isinstance(inner_args[0], ast.Name):
                var = inner_args[0].id
                # Allow already-resolved variables (naming convention: resolved_*)
                if not var.startswith("resolved_"):
                    violations.append(
                        f"Line {node.lineno}: Path({var}).resolve() is banned — "
                        f"use get_safe_path({var}) from mcp_server.path_utils for "
                        "cross-platform safe path resolution. Bare .resolve() silently "
                        "maps Unix paths to broken Windows paths."
                    )

    # Barcode package name shortcuts — all wrong
    if re.search(r"""['"]aspose-barcode['"]""", code) and "aspose-barcode-for-python-via-net" not in code:
        violations.append(
            "'aspose-barcode' found without '-for-python-via-net' suffix. "
            "Full package name required: aspose-barcode-for-python-via-net"
        )

    # --- Regex-based checks (belt-and-suspenders for patterns hard to catch via AST) ---
    # Skip lines that are obviously comments or doctest examples so that code
    # shown in docstrings (e.g. ">>> print(...)") doesn't generate false positives.
    for lineno, line in enumerate(code.splitlines(), start=1):
        stripped = line.lstrip()
        if stripped.startswith("#") or stripped.startswith(">>>") or stripped.startswith("..."):
            continue
        for pattern, message in _BANNED_PATTERNS:
            if re.search(pattern, line, re.MULTILINE):
                violations.append(f"Line {lineno}: {message}")

    return violations


def _collect_function_lines(tree: ast.AST, result: set[int]) -> None:
    """Collect line numbers of all function definitions.

    Args:
        tree: AST tree to walk.
        result: Set to populate with line numbers.
    """
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            result.add(node.lineno)


def _is_inside_function(node: ast.AST, tree: ast.AST) -> bool:
    """Check if an AST node is nested inside a function definition.

    Args:
        node: The node to check.
        tree: The full AST tree.

    Returns:
        True if the node is inside a function body.
    """
    # Build parent map
    parent_map: dict[int, ast.AST] = {}
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            parent_map[id(child)] = parent

    current: ast.AST | None = parent_map.get(id(node))
    while current is not None:
        if isinstance(current, (ast.FunctionDef, ast.AsyncFunctionDef)):
            return True
        current = parent_map.get(id(current))
    return False


def _get_call_name(node: ast.Call) -> str:
    """Extract the function name from a Call node.

    Args:
        node: AST Call node.

    Returns:
        Function name string, or empty string if not determinable.
    """
    if isinstance(node.func, ast.Name):
        return node.func.id
    if isinstance(node.func, ast.Attribute):
        return node.func.attr
    return ""
