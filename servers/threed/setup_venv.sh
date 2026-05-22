#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="${SCRIPT_DIR}/.venv"

echo "Setting up virtual environment for Aspose.3D MCP Server..."
echo "Platform: cross-platform (Windows, Linux, macOS)"
echo "Package: aspose-3d (Python module: aspose.threed)"
echo "Location: ${VENV_DIR}"

python3 -m venv "${VENV_DIR}"
source "${VENV_DIR}/bin/activate"

echo "Installing dependencies..."
pip install --upgrade pip --quiet
pip install -r "${SCRIPT_DIR}/requirements.txt" --quiet

echo ""
echo "✓ Setup complete!"
echo ""
echo "To activate:"
echo "  source servers/threed/.venv/bin/activate"
echo ""
echo "To start the server (stdio):"
echo "  python servers/threed/server.py"
echo ""
echo "To start the server (HTTP on port 8007):"
echo "  python servers/threed/server.py --transport streamable-http --port 8007"
