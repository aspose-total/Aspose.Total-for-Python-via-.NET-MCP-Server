#!/usr/bin/env python3
"""Aspose.Email standalone MCP server.

Serves only the Email plugin — no other Aspose products required.
Cross-platform: Windows, Linux, macOS.

PACKAGE NOTE: Use 'aspose-email-for-python-via-net' (the full long name).
NOT 'aspose-email-cloud' (cloud REST SDK requiring API credentials).
NOT 'aspose-email' (does not exist as a pip-installable .NET binding).

Usage:
    python servers/email/server.py                              # stdio
    python servers/email/server.py --transport streamable-http --port 8011
    python servers/email/server.py --transport sse --port 8011
"""
from __future__ import annotations

import argparse
import logging
import os
import sys
from pathlib import Path

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

_SERVER_DIR = Path(__file__).resolve().parent
load_dotenv(_SERVER_DIR / ".env")   # servers/email/.env — product-specific overrides
load_dotenv(_REPO_ROOT / ".env")    # repo-root .env — shared defaults (does not override)

from mcp.server.fastmcp import FastMCP  # type: ignore[import-untyped]
from mcp_server.plugins.email_plugin import EmailPlugin  # type: ignore[import-untyped]

_MCP_INSTRUCTIONS = (
    "This server reads, converts, and processes email files "
    "using Aspose.Email for Python via .NET. No email client software required. "
    "Supports MSG, EML, MHTML, HTML, PST, MBOX and other formats. "
    "All tools work with files already present in the server's ASPOSE_FILES_PATH folder. "
    "Pass only the bare filename (e.g. 'message.eml') to file parameters — never a full path. "
    "Output files are written to the same ASPOSE_FILES_PATH directory. "
    "Cross-platform: Windows, Linux, macOS."
)


def main() -> None:
    """Entry point for the Aspose Email standalone MCP server."""
    parser = argparse.ArgumentParser(description="Aspose Email standalone MCP server")
    parser.add_argument(
        "--transport",
        choices=["stdio", "streamable-http", "sse"],
        default="stdio",
    )
    parser.add_argument("--port", type=int, default=8011)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--mount-path", default="/mcp")
    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        default="INFO",
    )
    args = parser.parse_args()

    logging.getLogger().setLevel(getattr(logging, args.log_level))

    mcp = FastMCP("Aspose Email MCP Server", instructions=_MCP_INSTRUCTIONS)

    # Accept ASPOSE_FILES_PATH (standard env var shared by all servers).
    # The email plugin reads ASPOSE_INPUT_DIR / ASPOSE_OUTPUT_DIR internally,
    # so map both to the same directory.
    files_path = os.environ.get("ASPOSE_FILES_PATH", "").strip()
    if files_path:
        Path(files_path).mkdir(parents=True, exist_ok=True)
        os.environ["ASPOSE_INPUT_DIR"] = files_path
        os.environ["ASPOSE_OUTPUT_DIR"] = files_path
        logger.info("ASPOSE_FILES_PATH: %s", files_path)
    else:
        logger.warning("ASPOSE_FILES_PATH not set — email tools will not resolve input files.")

    # Accept ASPOSE_LICENSE_FILE (standard). The plugin reads ASPOSE_LICENSE_PATH internally.
    license_file = os.environ.get("ASPOSE_LICENSE_FILE", "").strip()
    if license_file:
        os.environ["ASPOSE_LICENSE_PATH"] = license_file
        if Path(license_file).is_file():
            logger.info("ASPOSE_LICENSE_FILE: %s", license_file)
        else:
            logger.warning("ASPOSE_LICENSE_FILE set but file not found: %s", license_file)
    else:
        logger.warning("ASPOSE_LICENSE_FILE not set — running in evaluation mode.")

    plugin = EmailPlugin()
    plugin.register_tools(mcp)

    logger.info("Aspose Email MCP Server starting (transport=%s)", args.transport)

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
