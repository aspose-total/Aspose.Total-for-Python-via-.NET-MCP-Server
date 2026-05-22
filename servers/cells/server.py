#!/usr/bin/env python3
"""Aspose Cells MCP Server — standalone single-plugin process.

Run from the project root with the cells venv active:
  servers\\cells\\.venv\\Scripts\\python.exe servers\\cells\\server.py
"""
from __future__ import annotations

import logging
import os
import sys
from pathlib import Path

# Add project root so mcp_server is importable without installation
_project_root = Path(__file__).resolve().parent.parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

logging.basicConfig(
    stream=sys.stderr,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

from dotenv import load_dotenv  # type: ignore[import-untyped]
load_dotenv(_project_root / ".env")

from mcp.server.fastmcp import FastMCP  # type: ignore[import-untyped]
import mcp_server.path_utils as path_utils
from mcp_server.plugins.cells_plugin import CellsPlugin

SERVER_VERSION = "0.1.0"
_MCP_INSTRUCTIONS = (
    "This server processes Excel spreadsheets using Aspose.Cells. "
    "All tools work with files already present in the server's ASPOSE_FILES_PATH folder. "
    "Pass only the bare filename (e.g. 'report.xlsx') to file parameters — never a full path. "
    "Output files are written to the same ASPOSE_FILES_PATH directory. "
    "Sheet indices are 0-based: sheet_index=0 is the first sheet."
)


def main() -> None:
    mcp = FastMCP("Aspose Cells MCP Server", instructions=_MCP_INSTRUCTIONS)

    plugin = CellsPlugin()
    plugin.register_tools(mcp)
    logger.info("Registered %d tools from cells plugin.", len(plugin.get_tool_manifest()))

    files_path = os.environ.get("ASPOSE_FILES_PATH")
    if files_path:
        path_utils.FILES_BASE_PATH = files_path
        Path(files_path).mkdir(parents=True, exist_ok=True)
        logger.info("Path mode: SANDBOX — files resolved against: %s", files_path)
    else:
        logger.info("Path mode: LOCAL — pass full absolute paths to tools.")

    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
