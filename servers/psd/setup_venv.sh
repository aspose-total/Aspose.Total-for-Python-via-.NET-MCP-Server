#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="${SCRIPT_DIR}/.venv"

echo "Setting up virtual environment for Aspose.PSD MCP Server..."
echo "Platform: cross-platform (Windows x32/x64, Linux x64, macOS x64/Arm64)"
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
echo "  source servers/psd/.venv/bin/activate"
echo ""
echo "To start the server (stdio):"
echo "  python servers/psd/server.py"
echo ""
echo "To start the server (HTTP on port 8004):"
echo "  python servers/psd/server.py --transport streamable-http --port 8004"
