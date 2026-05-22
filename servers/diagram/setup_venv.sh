#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="${SCRIPT_DIR}/.venv"

echo "Setting up virtual environment for Aspose.Diagram MCP Server..."
echo "Platform: cross-platform (Windows, Linux, macOS)"
echo ""
echo "PACKAGE NOTE: Installing 'aspose-diagram-python' (with -python suffix)"
echo "  NOT 'aspose-diagram'       — that is the Java/JPype variant requiring a JVM"
echo "  NOT 'aspose-diagram-cloud' — that requires cloud API credentials"
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
echo "  source servers/diagram/.venv/bin/activate"
echo ""
echo "To start the server (stdio):"
echo "  python servers/diagram/server.py"
echo ""
echo "To start the server (HTTP on port 8010):"
echo "  python servers/diagram/server.py --transport streamable-http --port 8010"
