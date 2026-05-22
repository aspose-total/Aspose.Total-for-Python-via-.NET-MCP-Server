#!/usr/bin/env python3
"""Aspose MCP Server — single FastMCP process with dynamic plugin loading.

All logging goes to stderr. Nothing is written to stdout except valid MCP JSON frames.
"""

from __future__ import annotations

import argparse
import importlib
import logging
import sys
from pathlib import Path

# ALL logging must go to stderr. Set this before any other imports.
logging.basicConfig(
    stream=sys.stderr,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

logger = logging.getLogger(__name__)

from mcp.server.fastmcp import FastMCP  # type: ignore[import-untyped]  # noqa: E402

from mcp_server.config import AsposeConfig, load_config  # noqa: E402
from mcp_server.plugin import AsposePlugin  # noqa: E402
from mcp_server.validators.path_safety import check_path_safety  # noqa: E402
import mcp_server.path_utils as path_utils  # noqa: E402

SERVER_VERSION = "0.2.0"

# Aspose packages all share aspose.pyreflection — they must be at the same version.
_ASPOSE_PYPI_PACKAGES = [
    "aspose-ocr-python-net",
    "aspose-zip",
    "aspose-imaging-python-net",
    "aspose-words",
    "aspose-pdf",
    "aspose-cells-python",
    "aspose-slides",
]


def _warn_aspose_version_conflicts() -> None:
    """Log a warning if any installed Aspose packages are at different versions.

    All Aspose Python-via-.NET packages share the aspose.pyreflection C extension.
    Mismatched versions cause ImportError -1009 at runtime when a second package
    tries to load a capsule that the first package's version of pyreflection
    no longer exposes.

    Args:
        None

    Returns:
        None

    Raises:
        None. Errors during version lookup are silently ignored.

    Example:
        >>> _warn_aspose_version_conflicts()
    """
    try:
        from importlib.metadata import packages_distributions, version as pkg_version
        installed: dict[str, str] = {}
        for pkg in _ASPOSE_PYPI_PACKAGES:
            try:
                installed[pkg] = pkg_version(pkg)
            except Exception:  # noqa: BLE001
                pass
        versions = set(installed.values())
        if len(versions) > 1:
            logger.warning(
                "Aspose package version MISMATCH detected — this will cause "
                "ImportError (-1009) when multiple products are loaded. "
                "All packages must be the same version. Found: %s. "
                "Fix: pip install %s",
                installed,
                " ".join(f'"{p}=={max(versions)}"' for p in installed),
            )
    except Exception:  # noqa: BLE001
        pass

# Map product_id → plugin module and class name.
# NOTE: words uses pyreflection 25.8.0.0; zip/ocr/imaging use 24.5.3.0.
# Running words alongside the others in the SAME process will cause an
# ImportError. Use separate server processes (servers/{product}/server.py).
_PLUGIN_MAP: dict[str, tuple[str, str]] = {
    "ocr": ("mcp_server.plugins.ocr_plugin", "OcrPlugin"),
    "zip": ("mcp_server.plugins.zip_plugin", "ZipPlugin"),
    "imaging": ("mcp_server.plugins.imaging_plugin", "ImagingPlugin"),
    "words": ("mcp_server.plugins.words_plugin", "WordsPlugin"),
    "slides": ("mcp_server.plugins.slides_plugin", "SlidesPlugin"),
    "pdf": ("mcp_server.plugins.pdf_plugin", "PdfPlugin"),
}

_PYPI_MAP: dict[str, str] = {
    "ocr": "aspose-ocr-python-net",
    "words": "aspose-words",
    "pdf": "aspose-pdf",
    "cells": "aspose-cells-python",
    "slides": "aspose-slides",
    "email": "Aspose.Email-for-Python-via-NET",
    "imaging": "aspose-imaging-python-net",
    "barcode": "aspose-barcode",
    "cad": "aspose-cad",
    "threed": "aspose-3d",
    "html": "aspose-html",
    "psd": "aspose-psd",
    "svg": "aspose-svg-net",
    "diagram": "aspose-diagram",
    "tasks": "aspose-tasks",
    "gis": "aspose-gis",
    "zip": "aspose-zip",
    "finance": "aspose-finance",
    "page": "aspose-page",
}


def _resolve_products(products: list[str]) -> list[str]:
    """Expand 'all' keyword to all known plugin product IDs.

    Args:
        products: List of product IDs, possibly containing "all".

    Returns:
        Expanded list of product IDs.
    """
    if "all" in products:
        return list(_PLUGIN_MAP.keys())
    return products


def load_plugins(config: AsposeConfig, mcp: FastMCP) -> dict[str, AsposePlugin]:
    """Discover, import, and register all enabled plugins.

    For each product_id in config.products:
      1. Check if plugin module exists.
      2. Attempt to import the plugin class.
      3. If package is missing: log WARNING to stderr, skip.
      4. If plugin module missing: log WARNING to stderr, skip.
      5. If both present: instantiate plugin, call register_tools(mcp).
      6. Run path_safety_check at startup; log WARNING for any violations.

    Never raises — always continues loading remaining plugins.

    Args:
        config: The loaded server configuration.
        mcp: The FastMCP server instance.

    Returns:
        Dict of {product_id: plugin_instance} for successfully loaded plugins.
    """
    loaded: dict[str, AsposePlugin] = {}
    products = _resolve_products(config.products)

    for product_id in products:
        if product_id not in _PLUGIN_MAP:
            logger.warning("Unknown product_id %r — no plugin registered. Skipping.", product_id)
            continue

        module_path, class_name = _PLUGIN_MAP[product_id]
        pypi_pkg = _PYPI_MAP.get(product_id, "unknown")

        # Check if the plugin module file exists.
        # Use __file__ to build an absolute path — relative paths break when
        # the server is spawned by a host (e.g. Claude Desktop) from a
        # different working directory.
        module_file = Path(__file__).parent / "plugins" / f"{product_id}_plugin.py"
        if not module_file.is_file():
            logger.warning(
                "Plugin file not found for %r: %s. Skipping.", product_id, module_file
            )
            continue

        try:
            mod = importlib.import_module(module_path)
        except ImportError as exc:
            logger.warning(
                "Package %s not installed (required for %r plugin). "
                "Install with: pip install '%s'. Skipping. Error: %s",
                pypi_pkg,
                product_id,
                pypi_pkg,
                exc,
            )
            continue
        except Exception as exc:  # noqa: BLE001
            logger.warning(
                "Failed to import plugin module %r for %r: %s. Skipping.",
                module_path,
                product_id,
                exc,
            )
            continue

        try:
            plugin_class = getattr(mod, class_name)
            plugin: AsposePlugin = plugin_class()
        except Exception as exc:  # noqa: BLE001
            logger.warning(
                "Failed to instantiate plugin class %r for %r: %s. Skipping.",
                class_name,
                product_id,
                exc,
            )
            continue

        # Run path safety check on plugin source
        plugin_source = module_file.read_text(encoding="utf-8")
        violations = check_path_safety(plugin_source)
        if violations:
            for violation in violations:
                logger.warning("Path safety violation in %s plugin: %s", product_id, violation)

        try:
            plugin.register_tools(mcp)
        except Exception as exc:  # noqa: BLE001
            logger.warning(
                "Failed to register tools for %r plugin: %s. Skipping.", product_id, exc
            )
            continue

        manifest = plugin.get_tool_manifest()
        loaded[product_id] = plugin
        logger.info(
            "Loaded plugin: %s (%d tools)",
            product_id,
            len(manifest),
        )

    if not loaded:
        logger.warning("No plugins were loaded. The server will start with zero tools.")
    else:
        logger.info("Total plugins loaded: %d — %s", len(loaded), list(loaded.keys()))

    return loaded


def build_mcp_server(config: AsposeConfig) -> tuple[FastMCP, dict[str, AsposePlugin]]:
    """Build the FastMCP server with all enabled plugins registered.

    Args:
        config: The loaded server configuration.

    Returns:
        Tuple of (FastMCP instance, loaded plugins dict).
    """
    mcp = FastMCP(
        "Aspose MCP Server",
        instructions=(
            "This server processes files using Aspose APIs. "
            "IMPORTANT: All tools work with files that are already present in the server's ASPOSE_FILES_PATH folder. "
            "You MUST NOT ask the user to upload files — the user places files in that folder directly. "
            "Always pass only the bare filename (e.g. 'report.pdf', 'photo.jpg') to every tool parameter that ends with _filename. "
            "Never pass full paths, drive letters, or directory components. "
            "Output files are also written to ASPOSE_FILES_PATH; the tool returns the bare output filename."
        ),
    )
    _warn_aspose_version_conflicts()
    loaded = load_plugins(config, mcp)

    # Register /health as a resource for HTTP transports
    @mcp.resource("health://status")
    def health_resource() -> str:
        """Return server health status as a JSON string."""
        import json

        pkg_versions: dict[str, str] = {}
        tool_counts: dict[str, int] = {}
        for pid, plg in loaded.items():
            tool_counts[pid] = len(plg.get_tool_manifest())
            try:
                import importlib.metadata as meta
                pkg_versions[_PYPI_MAP.get(pid, pid)] = meta.version(
                    _PYPI_MAP.get(pid, pid)
                )
            except Exception:  # noqa: BLE001
                pkg_versions[_PYPI_MAP.get(pid, pid)] = "unknown"

        return json.dumps(
            {
                "status": "ok",
                "server_version": SERVER_VERSION,
                "loaded_plugins": list(loaded.keys()),
                "tool_counts": tool_counts,
                "package_versions": pkg_versions,
                "transport": config.server.transport,
            },
            indent=2,
        )

    return mcp, loaded


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse CLI arguments for the MCP server.

    Args:
        argv: Argument list. Defaults to sys.argv[1:].

    Returns:
        Parsed namespace.
    """
    parser = argparse.ArgumentParser(
        description="Aspose MCP Server — FastMCP server with dynamic plugin loading",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--products",
        nargs="+",
        metavar="PRODUCT",
        help='Product IDs to load. Use "all" for all installed plugins.',
    )
    parser.add_argument(
        "--transport",
        choices=["stdio", "streamable-http", "sse"],
        default=None,
        help="MCP transport protocol (default: stdio).",
    )
    parser.add_argument(
        "--host",
        default=None,
        help="Bind host for HTTP transports (default: 127.0.0.1).",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=None,
        help="Port for HTTP transports (default: 8000).",
    )
    parser.add_argument(
        "--mount-path",
        default=None,
        dest="mount_path",
        help="URL path for streamable-http transport (default: /mcp).",
    )
    parser.add_argument(
        "--stateless",
        action="store_true",
        default=False,
        help="Enable stateless HTTP mode (for load balancers).",
    )
    parser.add_argument(
        "--config",
        default=None,
        metavar="PATH",
        help="Path to aspose_mcp_config.yaml.",
    )
    parser.add_argument(
        "--files-path",
        default=None,
        dest="files_path",
        metavar="DIR",
        help=(
            "Base directory for all file I/O (overrides ASPOSE_FILES_PATH env var). "
            "When set, callers pass relative filenames; the server resolves them here."
        ),
    )
    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        default="INFO",
        dest="log_level",
        help="Logging level (default: INFO).",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    """Entry point for the Aspose MCP Server.

    Args:
        argv: CLI argument list. Defaults to sys.argv[1:].
    """
    args = parse_args(argv)

    # Set log level
    logging.getLogger().setLevel(getattr(logging, args.log_level))

    config = load_config(
        config_path=args.config,
        products_override=args.products,
        transport_override=args.transport,
        host_override=args.host,
        port_override=args.port,
        mount_path_override=args.mount_path,
        stateless_override=args.stateless if args.stateless else None,
        files_path_override=args.files_path,
    )

    logger.info(
        "Starting Aspose MCP Server v%s — transport=%s, products=%s",
        SERVER_VERSION,
        config.server.transport,
        config.products,
    )

    mcp, _loaded = build_mcp_server(config)

    # Activate sandboxed (relative-path) mode when a files directory is configured.
    # Priority: --files-path CLI flag > ASPOSE_FILES_PATH env var > aspose.files_path
    # in the YAML config file.  All three are already resolved into config.files_path
    # by load_config(), so we only need to check that single field here.
    aspose_files_path = config.files_path
    if aspose_files_path:
        path_utils.FILES_BASE_PATH = aspose_files_path
        try:
            Path(path_utils.FILES_BASE_PATH).mkdir(parents=True, exist_ok=True)
        except OSError as exc:
            logger.warning(
                "Could not create ASPOSE_FILES_PATH directory %r: %s — "
                "it must already exist and be writable.",
                path_utils.FILES_BASE_PATH, exc,
            )
        logger.info(
            "Path mode: SANDBOX — all I/O resolved against: %s  "
            "(callers pass filenames only, e.g. 'scan.jpg')",
            path_utils.FILES_BASE_PATH,
        )
    else:
        logger.info(
            "Path mode: LOCAL — ASPOSE_FILES_PATH not set.  "
            "Callers must pass full absolute paths (e.g. C:\\Users\\...\\scan.jpg)."
        )

    transport = config.server.transport

    if transport == "stdio":
        mcp.run(transport="stdio")

    elif transport == "streamable-http":
        if not aspose_files_path:
            # Fall back to a writable directory in the user's home folder.
            # NEVER use a relative path like "./server_files" — the process CWD
            # when launched by Claude Desktop or other hosts is often a system
            # directory where the process has no write permission.
            _default = Path.home() / "aspose_mcp_files"
            path_utils.FILES_BASE_PATH = str(_default)
            _default.mkdir(parents=True, exist_ok=True)
            logger.info(
                "Network mode: ASPOSE_FILES_PATH not set — "
                "defaulting files dir to: %s", path_utils.FILES_BASE_PATH
            )
        mcp.run(
            transport="streamable-http",
            host=config.server.host,
            port=config.server.port,
            path=config.server.mount_path or "/mcp",
        )

    elif transport == "sse":
        if not aspose_files_path:
            _default = Path.home() / "aspose_mcp_files"
            path_utils.FILES_BASE_PATH = str(_default)
            _default.mkdir(parents=True, exist_ok=True)
            logger.info(
                "Network mode: ASPOSE_FILES_PATH not set — "
                "defaulting files dir to: %s", path_utils.FILES_BASE_PATH
            )
        mcp.run(
            transport="sse",
            host=config.server.host,
            port=config.server.port,
        )

    else:
        logger.error("Unknown transport: %r. Use stdio, streamable-http, or sse.", transport)
        sys.exit(1)


if __name__ == "__main__":
    main()
