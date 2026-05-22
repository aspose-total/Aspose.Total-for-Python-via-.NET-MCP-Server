#!/usr/bin/env python3
"""Aspose.TeX standalone MCP server.

Serves only the TeX/LaTeX plugin — no other Aspose products required.
Import path assumes this file is run from the repo root or the
servers/tex/ directory, both of which have mcp_server/ accessible.

PLATFORM NOTE: aspose-tex-net is Windows only (x86/x64).
This server will start on any platform but the tex plugin will report
health_check() = False on Linux/macOS. All tools will raise
RuntimeError on non-Windows platforms.

Usage:
    python servers/tex/server.py                              # stdio
    python servers/tex/server.py --transport streamable-http --port 8002
    python servers/tex/server.py --transport sse --port 8002
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
from mcp_server.plugins.tex_plugin import TexPlugin  # type: ignore[import-untyped]

_MCP_INSTRUCTIONS = (
    "This server converts TeX/LaTeX files and renders math formulas using Aspose.TeX. "
    "All tools work with files already present in the server's ASPOSE_INPUT_DIR folder. "
    "Pass only the bare filename (e.g. 'document.tex') to file parameters — never a full path. "
    "Output files are written to ASPOSE_OUTPUT_DIR. "
    "PLATFORM: Windows only (x86/x64). Tools raise RuntimeError on Linux/macOS."
)


def main() -> None:
    """Entry point for the Aspose TeX standalone MCP server."""
    import argparse

    parser = argparse.ArgumentParser(description="Aspose TeX standalone MCP server")
    parser.add_argument(
        "--transport",
        choices=["stdio", "streamable-http", "sse"],
        default="stdio",
    )
    parser.add_argument("--port", type=int, default=8002)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--mount-path", default="/mcp")
    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        default="INFO",
    )
    args = parser.parse_args()

    logging.getLogger().setLevel(getattr(logging, args.log_level))

    mcp = FastMCP("Aspose TeX MCP Server", instructions=_MCP_INSTRUCTIONS)

    plugin = TexPlugin()
    plugin.register_tools(mcp)

    files_path = os.environ.get("ASPOSE_FILES_PATH")
    if files_path:
        path_utils.FILES_BASE_PATH = files_path
        Path(files_path).mkdir(parents=True, exist_ok=True)
        logger.info("Path mode: SANDBOX — files resolved against: %s", files_path)
    else:
        logger.info("Path mode: LOCAL — pass full absolute paths to tools.")

    logger.info("Aspose TeX MCP Server starting (transport=%s)", args.transport)

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
