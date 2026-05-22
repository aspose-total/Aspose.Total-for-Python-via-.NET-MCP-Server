#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="${SCRIPT_DIR}/.venv"

echo "Setting up virtual environment for Aspose.Email MCP Server..."
echo "Platform: cross-platform (Windows, Linux, macOS)"
echo ""
echo "PACKAGE NOTE: Installing 'aspose-email-for-python-via-net' (full long name)"
echo "  NOT 'aspose-email-cloud' — that requires Aspose Cloud API credentials"
echo "  NOT 'aspose-email'       — that package does not exist as a .NET binding"
echo ""
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
echo "  source servers/email/.venv/bin/activate"
echo ""
echo "To start the server (stdio):"
echo "  python servers/email/server.py"
echo ""
echo "To start the server (HTTP on port 8011):"
echo "  python servers/email/server.py --transport streamable-http --port 8011"
