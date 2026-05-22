"""Configuration loader for the Aspose MCP Server.

Searches for config in this order:
  1. Explicit --config CLI path
  2. Current working directory (aspose_mcp_config.yaml)
  3. ~/.config/aspose/aspose_mcp_config.yaml
  4. ~/aspose_mcp_config.yaml

CLI flags and environment variables override config file values.

``files_path`` resolution priority (highest → lowest):
  1. CLI ``--files-path`` flag (passed as ``files_path_override``)
  2. ``ASPOSE_FILES_PATH`` environment variable
  3. ``aspose.files_path`` in the YAML config file
  4. ``None`` (stdio local-mode: callers must pass full absolute paths)
"""

from __future__ import annotations

import logging
import os
from dataclasses import dataclass, field
from pathlib import Path

import yaml  # type: ignore[import-untyped]

logger = logging.getLogger(__name__)

_DEFAULT_CONFIG_NAME = "aspose_mcp_config.yaml"
_SEARCH_DIRS = [
    Path.cwd(),
    Path.home() / ".config" / "aspose",
    Path.home(),
]


@dataclass
class ServerConfig:
    """Parsed server configuration."""

    host: str = "127.0.0.1"
    port: int = 8000
    transport: str = "stdio"
    mount_path: str = "/mcp"
    stateless: bool = False


@dataclass
class AsposeConfig:
    """Top-level Aspose MCP configuration."""

    license_path: str | None = None
    files_path: str | None = None
    products: list[str] = field(default_factory=lambda: ["ocr"])
    server: ServerConfig = field(default_factory=ServerConfig)


def _find_config_file() -> Path | None:
    """Search standard locations for the config file.

    Returns:
        Path to the config file if found, None otherwise.
    """
    for directory in _SEARCH_DIRS:
        candidate = directory / _DEFAULT_CONFIG_NAME
        if candidate.is_file():
            logger.debug("Found config file at: %s", candidate)
            return candidate
    return None


def load_config(
    config_path: str | Path | None = None,
    *,
    products_override: list[str] | None = None,
    transport_override: str | None = None,
    host_override: str | None = None,
    port_override: int | None = None,
    mount_path_override: str | None = None,
    stateless_override: bool | None = None,
    files_path_override: str | None = None,
) -> AsposeConfig:
    """Load and merge configuration from file and CLI overrides.

    ``files_path`` resolution priority (highest → lowest):
      1. ``files_path_override`` (CLI ``--files-path``)
      2. ``ASPOSE_FILES_PATH`` environment variable
      3. ``aspose.files_path`` in the YAML config file
      4. ``None``

    Args:
        config_path: Explicit path to the config file. If None, searches standard locations.
        products_override: CLI --products override. "all" expands to all installed products.
        transport_override: CLI --transport override.
        host_override: CLI --host override.
        port_override: CLI --port override.
        mount_path_override: CLI --mount-path override.
        stateless_override: CLI --stateless override.
        files_path_override: CLI --files-path override.

    Returns:
        Merged AsposeConfig instance.
    """
    raw: dict[object, object] = {}

    if config_path is not None:
        resolved = Path(config_path).resolve()
        if resolved.is_file():
            with resolved.open(encoding="utf-8") as fh:
                raw = yaml.safe_load(fh) or {}
            logger.info("Loaded config from: %s", resolved)
        else:
            logger.warning("Config file not found at: %s — using defaults", resolved)
    else:
        found = _find_config_file()
        if found:
            with found.open(encoding="utf-8") as fh:
                raw = yaml.safe_load(fh) or {}
            logger.info("Loaded config from: %s", found)
        else:
            logger.info("No config file found — using defaults")

    aspose_section = raw.get("aspose", {})
    if not isinstance(aspose_section, dict):
        aspose_section = {}

    server_section = aspose_section.get("server", {})
    if not isinstance(server_section, dict):
        server_section = {}

    # Build server config
    server = ServerConfig(
        host=str(server_section.get("host", "127.0.0.1")),
        port=int(str(server_section.get("port", 8000))),
        transport=str(server_section.get("transport", "stdio")),
        mount_path=str(server_section.get("mount_path", "/mcp")),
        stateless=bool(server_section.get("stateless", False)),
    )

    # Apply CLI overrides to server
    if transport_override is not None:
        server.transport = transport_override
    if host_override is not None:
        server.host = host_override
    if port_override is not None:
        server.port = port_override
    if mount_path_override is not None:
        server.mount_path = mount_path_override
    if stateless_override is not None:
        server.stateless = stateless_override

    # Parse products
    raw_products = aspose_section.get("products", ["ocr"])
    if isinstance(raw_products, str):
        products: list[str] = [raw_products]
    elif isinstance(raw_products, list):
        products = [str(p) for p in raw_products]
    else:
        products = ["ocr"]

    if products_override is not None:
        products = products_override

    # "all" is handled at load time in server.py which knows which plugins exist
    license_path_raw = aspose_section.get("license_path")
    license_path = str(license_path_raw) if license_path_raw is not None else None

    # files_path: CLI override → ASPOSE_FILES_PATH env var → YAML value → None
    files_path_raw = aspose_section.get("files_path")
    files_path: str | None = str(files_path_raw) if files_path_raw is not None else None
    env_files_path = os.environ.get("ASPOSE_FILES_PATH")
    if env_files_path:
        files_path = env_files_path
    if files_path_override is not None:
        files_path = files_path_override

    return AsposeConfig(
        license_path=license_path,
        files_path=files_path,
        products=products,
        server=server,
    )
