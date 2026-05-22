#!/usr/bin/env python3
"""Aspose.Finance standalone MCP server.

Serves only the Finance plugin — no other Aspose products required.
Cross-platform: Windows x32/x64, Linux, Unix/macOS.

NOTE: aspose-finance requires Python >=3.5 and <3.12.

Usage:
    python servers/finance/server.py                              # stdio
    python servers/finance/server.py --transport streamable-http --port 8006
    python servers/finance/server.py --transport sse --port 8006
"""
from __future__ import annotations

import argparse
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
from mcp_server.plugins.finance_plugin import FinancePlugin  # type: ignore[import-untyped]

_MCP_INSTRUCTIONS = (
    "This server processes XBRL, iXBRL, and OFX financial document formats using Aspose.Finance. "
    "All tools work with files already present in the server's ASPOSE_INPUT_DIR folder. "
    "Pass only the bare filename (e.g. 'report.xbrl') to file parameters — never a full path. "
    "Output files are written to ASPOSE_OUTPUT_DIR. "
    "Cross-platform: Windows x32/x64, Linux, Unix/macOS. "
    "NOTE: aspose-finance requires Python >=3.5 and <3.12."
)


def main() -> None:
    """Entry point for the Aspose Finance standalone MCP server."""
    parser = argparse.ArgumentParser(description="Aspose Finance standalone MCP server")
    parser.add_argument(
        "--transport",
        choices=["stdio", "streamable-http", "sse"],
        default="stdio",
    )
    parser.add_argument("--port", type=int, default=8006)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--mount-path", default="/mcp")
    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        default="INFO",
    )
    args = parser.parse_args()

    logging.getLogger().setLevel(getattr(logging, args.log_level))

    mcp = FastMCP("Aspose Finance MCP Server", instructions=_MCP_INSTRUCTIONS)

    files_path = os.environ.get("ASPOSE_FILES_PATH", "").strip()
    if files_path:
        path_utils.FILES_BASE_PATH = files_path
        Path(files_path).mkdir(parents=True, exist_ok=True)
        logger.info("ASPOSE_FILES_PATH: %s", files_path)
    else:
        logger.warning("ASPOSE_FILES_PATH not set — tools will use working directory.")

    license_file = os.environ.get("ASPOSE_LICENSE_FILE", "").strip()
    if license_file and Path(license_file).is_file():
        logger.info("ASPOSE_LICENSE_FILE: %s", license_file)
    elif license_file:
        logger.warning("ASPOSE_LICENSE_FILE set but file not found: %s", license_file)
    else:
        logger.warning("ASPOSE_LICENSE_FILE not set — running in evaluation mode.")

    plugin = FinancePlugin()
    plugin.register_tools(mcp)

    logger.info("Aspose Finance MCP Server starting (transport=%s)", args.transport)

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
