"""Abstract base class for all Aspose product plugins."""

from abc import ABC, abstractmethod

from mcp.server.fastmcp import FastMCP  # type: ignore[import-untyped]


class AsposePlugin(ABC):
    """Abstract base class for all Aspose product plugins.

    Every plugin must implement all three abstract methods.
    Every @tool function in a plugin must follow the rules in IMPLEMENTATION NOTES.

    IMPLEMENTATION NOTES for all @tool functions:
    1. LAZY IMPORTS: import aspose.* inside each tool function, never at module level.
    2. NO STDOUT: use logging.getLogger(__name__) only. No print() anywhere.
    3. FILENAME-ONLY PARAMS: name file/folder params *_filename or *_folder_name.
       At the TOP of every tool body, sanitize each such param:
           param = Path(param.strip().replace('\x00', '')).name
       Then resolve with get_safe_path(param) from mcp_server.path_utils.
       NEVER use Path(p).resolve() or os.path.abspath() — they bypass sandbox mode.
    4. DEFAULT OUTPUT: use temp_output_path(stem, suffix, prefix="aspose_X_") from
       mcp_server.path_utils — NOT tempfile.gettempdir(). temp_output_path places
       output inside FILES_BASE_PATH so callers can find it alongside their inputs.
    5. VALIDATE INPUT: check Path(resolved_path).is_file() before calling Aspose.
    6. CREATE OUTPUT DIR: Path(resolved_output).parent.mkdir(parents=True, exist_ok=True).
    7. RETURN RESOLVED PATH: always include output_filename (resolved path) in result dict.
    8. NO OS.GETCWD: never use os.getcwd(); never construct paths relative to CWD.
    """

    product_name: str  # e.g. "ocr"  — used as tool name prefix
    pypi_package: str  # e.g. "aspose-ocr-python-net"
    min_version: str  # e.g. "24.3.0"

    @abstractmethod
    def register_tools(self, mcp: FastMCP) -> None:
        """Register all @tool-decorated functions with the FastMCP instance.

        Args:
            mcp: The FastMCP server instance to register tools with.
        """

    @abstractmethod
    def health_check(self) -> bool:
        """Return True if the Aspose package is importable and functional.

        Returns:
            True if the package is available and functional, False otherwise.
        """

    @abstractmethod
    def get_tool_manifest(self) -> list[dict[str, object]]:
        """Return structured tool list for evaluation and documentation generation.

        Each dict must have keys:
          name: str           — full tool name, e.g. "ocr_recognise_image_file"
          description: str    — one-sentence description for the MCP client
          params: list[dict]  — [{"name": str, "type": str, "required": bool,
                                   "description": str}]
          returns: str        — description of return value

        Returns:
            List of tool manifest dicts, one per registered tool.
        """


# Backwards-compatibility alias — older plugins (ocr, zip) import BasePlugin
BasePlugin = AsposePlugin
