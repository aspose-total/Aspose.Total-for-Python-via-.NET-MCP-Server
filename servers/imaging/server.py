#!/usr/bin/env python3
"""Aspose Imaging MCP Server — standalone single-plugin process."""
from __future__ import annotations

import logging
import os
import sys
from pathlib import Path

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
from mcp_server.plugins.imaging_plugin import ImagingPlugin

SERVER_VERSION = "0.1.0"
_MCP_INSTRUCTIONS = (
    "This server processes images using Aspose.Imaging. "
    "All tools work with files already present in the server's ASPOSE_FILES_PATH folder. "
    "Pass only the bare filename (e.g. 'photo.jpg') to file parameters — never a full path. "
    "Output files are written to the same ASPOSE_FILES_PATH directory."
)


def main() -> None:
    mcp = FastMCP("Aspose Imaging MCP Server", instructions=_MCP_INSTRUCTIONS)

    plugin = ImagingPlugin()
    plugin.register_tools(mcp)
    logger.info("Registered %d tools from imaging plugin.", len(plugin.get_tool_manifest()))

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
