"""Cross-platform path resolution utilities for Aspose MCP plugins.

The primary entry point for all filesystem path handling is :func:`get_safe_path`.
It operates in two modes controlled by the module-level :data:`FILES_BASE_PATH`
variable:

* **stdio / local mode** (``FILES_BASE_PATH is None``): the caller passes a full
  absolute path that already matches the server's OS (e.g. ``C:\\Users\\...``  on
  Windows or ``/home/...`` on Linux).  ``os.path.normpath`` normalises slashes;
  no OS-specific rejection is applied.

* **network mode** (SSE / HTTP, ``FILES_BASE_PATH`` is a directory string): the
  caller passes a *relative* path such as ``"reports/scan.jpg"``.  The server
  resolves it against ``FILES_BASE_PATH``, blocks path-traversal attacks, and
  rejects absolute paths from the caller.

Setting ``FILES_BASE_PATH`` via the ``ASPOSE_FILES_PATH`` environment variable
before starting the server is the recommended way to avoid path-format conflicts
when Claude Desktop and the MCP server run on different operating systems.

For cases where no shared filesystem exists at all, use :func:`decode_image_to_temp`
instead — the caller encodes the image as base64 and passes it directly over the
MCP protocol so no path resolution is needed.

Usage (inside a tool function):
    from mcp_server.path_utils import get_safe_path, decode_image_to_temp

    # Resolve an input path (works in both modes)
    full_path = get_safe_path(image_path)

    # Cross-OS: decode base64 image bytes written by the client
    tmp = decode_image_to_temp(image_data, "png")
    try:
        ...  # run OCR on tmp
    finally:
        tmp.unlink(missing_ok=True)
"""

from __future__ import annotations

import base64
import logging
import os
import sys
import tempfile
from pathlib import Path

logger = logging.getLogger(__name__)


def _on_windows() -> bool:
    """Return True when running on Windows."""
    return sys.platform == "win32"


# ---------------------------------------------------------------------------
# Mode control
# ---------------------------------------------------------------------------

# None  → stdio / local mode: caller passes a full absolute path.
# str   → network mode (SSE / HTTP): caller passes relative paths that are
#         resolved and sandboxed against this directory.
FILES_BASE_PATH: str | None = None

# ---------------------------------------------------------------------------
# License management
# ---------------------------------------------------------------------------

# Tracks which product IDs have already had their license applied so the
# apply_aspose_license() call inside register_tools() is a no-op on
# subsequent (hot-reload) invocations.
_LICENSE_APPLIED: set[str] = set()


def apply_aspose_license(product_id: str, aspose_module: object) -> None:
    """Apply an Aspose license from the ASPOSE_LICENSE_FILE environment variable.

    Call this once at plugin startup (e.g. inside ``register_tools``), passing
    the already-imported Aspose module.  Subsequent calls for the same
    *product_id* are cached no-ops.

    If ``ASPOSE_LICENSE_FILE`` is not set or the file does not exist the
    product continues to run in **evaluation mode** (watermarked output,
    size limits) — no exception is raised.

    Args:
        product_id: Short product identifier, e.g. ``"ocr"``, ``"words"``.
            Used for logging and deduplication only.
        aspose_module: The already-imported top-level Aspose module that
            exposes a ``License`` class, e.g. ``aspose.ocr``.

    Returns:
        None.

    Example:
        >>> import aspose.ocr as ocr
        >>> apply_aspose_license("ocr", ocr)  # applies once; noop on repeat calls
    """
    if product_id in _LICENSE_APPLIED:
        return

    _LICENSE_APPLIED.add(product_id)  # mark before any early returns

    license_path = os.environ.get("ASPOSE_LICENSE_FILE", "").strip()
    if not license_path:
        logger.info(
            "ASPOSE_LICENSE_FILE not set — Aspose.%s running in evaluation mode.",
            product_id.upper(),
        )
        return

    if not Path(license_path).is_file():
        logger.warning(
            "ASPOSE_LICENSE_FILE %r does not exist — Aspose.%s running in evaluation mode.",
            license_path,
            product_id.upper(),
        )
        return

    try:
        import io as _io
        lic = aspose_module.License()  # type: ignore[attr-defined]
        # Use BytesIO stream rather than a path string — .NET interop resolves
        # paths internally and can fail silently on forward-slash Windows paths.
        with open(license_path, "rb") as _f:
            lic.set_license(_io.BytesIO(_f.read()))
        logger.info(
            "Aspose.%s license applied from: %s", product_id.upper(), license_path
        )
    except Exception as exc:  # noqa: BLE001
        logger.warning(
            "Failed to apply Aspose.%s license from %r: %s — running in evaluation mode.",
            product_id.upper(),
            license_path,
            exc,
        )


def apply_license_for(product_module: str) -> bool:
    """Apply the Aspose license for a specific product by module name.

    Product-agnostic license helper for plugins introduced in Sprint 5+.
    Uses dynamic import so callers do not need to import the module first.
    Subsequent calls for the same product are cached no-ops.

    Args:
        product_module: Dotted Python module name, e.g. ``"aspose.slides"``,
            ``"aspose.words"``, ``"aspose.pdf"``.

    Returns:
        True if the license was applied successfully, False if running in
        evaluation mode (ASPOSE_LICENSE_FILE not set or file missing).

    Example:
        >>> from mcp_server.path_utils import apply_license_for
        >>> apply_license_for("aspose.slides")  # True or False
    """
    product_id = product_module.split(".")[-1]

    if product_id in _LICENSE_APPLIED:
        return True
    _LICENSE_APPLIED.add(product_id)

    license_path = os.environ.get("ASPOSE_LICENSE_FILE", "").strip()
    if not license_path:
        logger.info(
            "ASPOSE_LICENSE_FILE not set — %s running in evaluation mode.",
            product_module,
        )
        return False

    if not Path(license_path).is_file():
        logger.warning(
            "ASPOSE_LICENSE_FILE %r does not exist — %s running in evaluation mode.",
            license_path,
            product_module,
        )
        return False

    try:
        import importlib as _importlib  # noqa: PLC0415
        import io as _io  # noqa: PLC0415
        module = _importlib.import_module(product_module)
        license_class = getattr(module, "License")
        lic = license_class()
        with open(license_path, "rb") as _f:
            lic.set_license(_io.BytesIO(_f.read()))
        logger.info("%s license applied from: %s", product_module, license_path)
        return True
    except Exception as exc:  # noqa: BLE001
        logger.warning(
            "Failed to apply license for %r: %s — running in evaluation mode.",
            product_module,
            exc,
        )
        return False


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def get_safe_path(filename: str) -> str:
    """Resolve *filename* to a safe absolute path inside :data:`FILES_BASE_PATH`.

    All tools accept **filenames only** (e.g. ``"scan.jpg"``, ``"result.docx"``).
    The server combines the filename with :data:`FILES_BASE_PATH` (set via the
    ``ASPOSE_FILES_PATH`` environment variable) to form the full path.

    Absolute paths and paths that escape the base directory are always rejected.

    Args:
        filename: Plain filename or relative sub-path supplied by the MCP caller,
            e.g. ``"scan.jpg"`` or ``"subfolder/scan.jpg"``.

    Returns:
        Normalised absolute path string ready for filesystem I/O.

    Raises:
        ValueError: If ``ASPOSE_FILES_PATH`` is not configured, the filename is
            empty or invalid, contains a null byte, is an absolute path, or
            escapes the base directory via traversal (``../../``).

    Examples:
        >>> import mcp_server.path_utils as pu
        >>> pu.FILES_BASE_PATH = "C:/asposefiles"
        >>> get_safe_path("scan.jpg")
        'C:\\\\asposefiles\\\\scan.jpg'
        >>> get_safe_path("subfolder/doc.pdf")
        'C:\\\\asposefiles\\\\subfolder\\\\doc.pdf'
    """
    if not filename or "\x00" in filename:
        raise ValueError(f"Invalid filename: {filename!r}")

    if FILES_BASE_PATH is None:
        raise ValueError(
            "ASPOSE_FILES_PATH is not configured on the server.\n"
            "Add it to the env section of your Claude Desktop MCP config:\n"
            '  "ASPOSE_FILES_PATH": "C:/asposefiles"\n'
            "Then pass only a plain filename, e.g. 'scan.jpg'."
        )

    if os.path.isabs(filename):
        raise ValueError(
            f"Pass only a filename, not a full path: {filename!r}.\n"
            f"The server resolves filenames against ASPOSE_FILES_PATH automatically.\n"
            f"Example: 'scan.jpg' not 'C:\\\\Users\\\\...\\\\scan.jpg'."
        )

    base = os.path.realpath(FILES_BASE_PATH)
    candidate = os.path.realpath(os.path.join(base, filename))

    # Block path traversal (../../etc/passwd) and symlink escapes
    try:
        if os.path.commonpath([base, candidate]) != base:
            raise ValueError(f"Path escapes the allowed directory: {filename!r}")
    except ValueError:
        raise ValueError(f"Invalid path: {filename!r}")

    # Guard against writing a file to a path that is already a directory.
    # This produces an opaque UnauthorizedAccessException from .NET interop;
    # catching it here gives a clear message instead.
    if os.path.isdir(candidate):
        raise ValueError(
            f"Output path conflicts with an existing directory: {candidate!r}.\n"
            "A previous multi-page export created a folder with this name. "
            "Choose a different output filename."
        )

    return candidate


def resolve_path(path_str: str) -> Path:
    """Resolve *path_str* to an absolute :class:`~pathlib.Path`.

    .. deprecated::
        Use :func:`get_safe_path` instead.

    Args:
        path_str: Filename supplied by the MCP caller.

    Returns:
        Resolved absolute :class:`~pathlib.Path` inside :data:`FILES_BASE_PATH`.

    Raises:
        ValueError: If the path is empty, invalid, or ASPOSE_FILES_PATH is not set.
    """
    return Path(get_safe_path(path_str))


def temp_output_path(stem: str, suffix: str, prefix: str = "aspose_") -> Path:
    """Return a default output path for a generated file.

    When :data:`FILES_BASE_PATH` is set (sandbox / network mode), the path is
    placed inside that directory so the caller can find the output alongside their
    input files without knowing the server's filesystem layout.

    In local (stdio) mode where :data:`FILES_BASE_PATH` is ``None``, falls back
    to the OS temp directory — the absolute path is always returned in the tool
    response so the caller knows where to look.

    Args:
        stem: Base name component, e.g. ``"scan"`` or ``"invoice"``.
        suffix: File extension *including* the leading dot, e.g. ``".txt"``.
            Pass ``""`` for directory names.
        prefix: Prefix prepended to *stem* in the filename.  Default ``"aspose_"``.

    Returns:
        :class:`~pathlib.Path` inside :data:`FILES_BASE_PATH` (when set) or
        :func:`tempfile.gettempdir` (local mode).
    """
    filename = f"{prefix}{stem}{suffix}"
    base = FILES_BASE_PATH if FILES_BASE_PATH is not None else tempfile.gettempdir()
    return Path(base) / filename


def platform_hint() -> str:
    """Return a short path-format hint for error messages.

    Returns:
        Human-readable hint string reminding callers to pass filenames only.
    """
    base = FILES_BASE_PATH or "<ASPOSE_FILES_PATH not set>"
    return f"pass just the filename, e.g. 'scan.jpg' (server directory: {base})"


def decode_image_to_temp(image_data: str, image_format: str = "png") -> Path:
    """Decode base64 image data to a temporary file on the server.

    This is the recommended input method when the MCP client and server run on
    **different operating systems** (e.g. Claude on Linux, MCP server on Windows).
    The caller reads the image, encodes it as base64, and passes the string
    directly over the MCP protocol.  No filesystem path traversal is needed.

    Accepted input formats:

    * **Plain base64** — ``"/9j/4AAQSkZJRgAB..."``
    * **Data URI** — ``"data:image/jpeg;base64,/9j/4AAQSkZJRgAB..."``

    When a data URI is supplied the MIME type is used to infer the file
    extension automatically, overriding *image_format*.

    Aspose.OCR natively supports: PNG, JPEG, BMP, TIFF, GIF.
    Formats not supported by Aspose (e.g. **WebP**, AVIF, HEIC) are
    automatically converted to PNG via Pillow so the caller never has to
    think about format compatibility.

    Args:
        image_data: Base64-encoded image bytes, with or without a data URI prefix.
        image_format: File extension hint for the temp file (without the dot).
            Any common raster format is accepted — unsupported ones are
            converted to PNG automatically.  Default: ``"png"``.

    Returns:
        :class:`~pathlib.Path` pointing to a newly-created temporary file
        containing the decoded image bytes.  The **caller is responsible for
        deleting the file** when done (use ``path.unlink(missing_ok=True)``
        inside a ``finally`` block).

    Raises:
        ValueError: If *image_data* is empty, not valid base64, or the decoded
            bytes are suspiciously small (< 8 bytes, likely not a real image).

    Examples:
        >>> import base64, pathlib
        >>> data = base64.b64encode(b"fake-image-bytes").decode()
        >>> tmp = decode_image_to_temp(data, "png")
        >>> tmp.exists()
        True
        >>> tmp.unlink()
    """
    if not image_data or not image_data.strip():
        raise ValueError("image_data must not be empty")

    image_data = image_data.strip()

    # --- Strip data URI prefix and auto-detect format ---
    if image_data.startswith("data:"):
        header, _, payload = image_data.partition(",")
        # e.g. header = "data:image/jpeg;base64"
        if "/" in header:
            mime_subtype = header.split(";")[0].split("/")[-1].lower()
            if mime_subtype:
                image_format = mime_subtype
        image_data = payload

    # Normalise extension aliases
    image_format = image_format.lower().lstrip(".")
    if image_format == "jpeg":
        image_format = "jpg"

    # Formats Aspose.OCR accepts natively
    _ASPOSE_NATIVE = {"png", "jpg", "bmp", "tiff", "tif", "gif"}

    # --- Decode base64 ---
    try:
        # altchars handles URL-safe base64; padding is added defensively
        image_bytes = base64.b64decode(image_data + "==", altchars=b"-_", validate=False)
    except Exception as exc:
        raise ValueError(f"image_data is not valid base64: {exc}") from exc

    if len(image_bytes) < 8:
        raise ValueError(
            f"Decoded image data is only {len(image_bytes)} bytes — "
            "this is too small to be a real image. "
            "Check that the base64 string is complete."
        )

    # --- Convert formats Aspose cannot read (e.g. WebP, AVIF, HEIC) ---
    if image_format not in _ASPOSE_NATIVE:
        image_bytes, image_format = _convert_to_png(image_bytes, image_format)

    # --- Write to temp file ---
    suffix = f".{image_format}"
    fd, tmp_path_str = tempfile.mkstemp(prefix="aspose_ocr_b64_", suffix=suffix)
    try:
        with os.fdopen(fd, "wb") as fh:
            fh.write(image_bytes)
    except Exception:
        try:
            os.unlink(tmp_path_str)
        except OSError:
            pass
        raise

    return Path(tmp_path_str)


def _convert_to_png(image_bytes: bytes, source_format: str) -> tuple[bytes, str]:
    """Convert *image_bytes* to PNG using Pillow.

    Args:
        image_bytes: Raw image bytes in any format Pillow can read.
        source_format: Hint about the source format (e.g. "webp").  Used only
            in error messages.

    Returns:
        Tuple of (png_bytes, "png").

    Raises:
        ValueError: If Pillow is not installed or cannot decode the bytes.
    """
    try:
        from PIL import Image  # noqa: PLC0415
        import io  # noqa: PLC0415
    except ImportError as exc:
        raise ValueError(
            f"Image format {source_format!r} is not supported by Aspose.OCR natively "
            f"and Pillow is not installed for automatic conversion. "
            f"Install Pillow (pip install pillow) or convert the image to PNG/JPEG "
            f"before encoding it as base64."
        ) from exc

    try:
        import io  # noqa: PLC0415, F811
        with Image.open(io.BytesIO(image_bytes)) as img:
            # Convert palette or RGBA modes that PNG handles cleanly
            if img.mode not in ("RGB", "RGBA", "L", "LA"):
                img = img.convert("RGBA" if img.mode == "P" else "RGB")
            buf = io.BytesIO()
            img.save(buf, format="PNG")
            return buf.getvalue(), "png"
    except Exception as exc:
        raise ValueError(
            f"Could not convert {source_format!r} image to PNG: {exc}. "
            "Ensure the base64 data is a complete, valid image."
        ) from exc
