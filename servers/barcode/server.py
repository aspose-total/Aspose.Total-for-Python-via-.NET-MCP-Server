#!/usr/bin/env python3
"""Aspose.BarCode standalone MCP server.

Serves only the barcode plugin — no other Aspose products required.
Import path assumes this file is run from the repo root or the
servers/barcode/ directory, both of which have mcp_server/ accessible.

Usage:
    python servers/barcode/server.py                        # stdio
    python servers/barcode/server.py --transport streamable-http --port 8001
    python servers/barcode/server.py --transport sse --port 8001
"""
from __future__ import annotations

import logging
import os
import sys
from pathlib import Path

# Ensure mcp_server/ is importable regardless of working directory
_REPO_ROOT = Path(__file__).resolve().parent.parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

logging.basicConfig(
    stream=sys.stderr,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

from dotenv import load_dotenv  # type: ignore[import-untyped]
load_dotenv(_REPO_ROOT / ".env")

from mcp.server.fastmcp import FastMCP  # type: ignore[import-untyped]
import mcp_server.path_utils as path_utils
from mcp_server.plugins.barcode_plugin import BarcodePlugin  # type: ignore[import-untyped]

_MCP_INSTRUCTIONS = (
    "This server generates and recognizes barcodes using Aspose.BarCode. "
    "All tools work with files already present in the server's ASPOSE_FILES_PATH folder. "
    "Pass only the bare filename (e.g. 'barcode.png') to file parameters — never a full path. "
    "Output files are written to the same ASPOSE_FILES_PATH directory."
)


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Aspose BarCode standalone MCP server")
    parser.add_argument(
        "--transport",
        choices=["stdio", "streamable-http", "sse"],
        default="stdio",
    )
    parser.add_argument("--port", type=int, default=8001)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--mount-path", default="/mcp")
    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        default="INFO",
    )
    args = parser.parse_args()

    logging.getLogger().setLevel(getattr(logging, args.log_level))

    mcp = FastMCP("Aspose BarCode MCP Server", instructions=_MCP_INSTRUCTIONS)

    plugin = BarcodePlugin()
    plugin.register_tools(mcp)

    files_path = os.environ.get("ASPOSE_FILES_PATH")
    if files_path:
        path_utils.FILES_BASE_PATH = files_path
        Path(files_path).mkdir(parents=True, exist_ok=True)
        logger.info("Path mode: SANDBOX — files resolved against: %s", files_path)
    else:
        logger.info("Path mode: LOCAL — pass full absolute paths to tools.")

    if args.transport == "stdio":
        mcp.run(transport="stdio")
    elif args.transport == "streamable-http":
        mcp.run(
            transport="streamable-http",
            host=args.host,
            port=args.port,
            mount_path=args.mount_path,
        )
    elif args.transport == "sse":
        mcp.run(transport="sse", host=args.host, port=args.port)


if __name__ == "__main__":
    main()
