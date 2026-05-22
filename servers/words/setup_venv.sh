#!/usr/bin/env bash
# Setup virtual environment for Aspose Words standalone MCP server
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="${SCRIPT_DIR}/.venv"

echo "Setting up virtual environment for Aspose.Words MCP Server..."
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
echo "  source servers/words/.venv/bin/activate"
echo ""
echo "To start the server:"
echo "  servers/words/.venv/bin/python servers/words/server.py"
