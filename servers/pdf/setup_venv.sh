#!/usr/bin/env bash
# Setup virtual environment for Aspose PDF standalone MCP server
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="${SCRIPT_DIR}/.venv"

echo "Setting up virtual environment for Aspose.PDF MCP Server..."
echo "Location: ${VENV_DIR}"

python3 -m venv "${VENV_DIR}"
source "${VENV_DIR}/bin/activate"

echo "Installing dependencies..."
pip install --upgrade pip --quiet
pip install -r "${SCRIPT_DIR}/requirements.txt" --quiet

echo ""
echo "Setup complete!"
echo ""
echo "To activate the venv:"
echo "  source servers/pdf/.venv/bin/activate"
echo ""
echo "To start the server:"
echo "  servers/pdf/.venv/bin/python servers/pdf/server.py"
