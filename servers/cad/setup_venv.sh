#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="${SCRIPT_DIR}/.venv"

# Check Python version — aspose-cad requires Python >= 3.9
PYTHON_MAJOR=$(python3 -c "import sys; print(sys.version_info.major)")
PYTHON_MINOR=$(python3 -c "import sys; print(sys.version_info.minor)")
PYTHON_VERSION="${PYTHON_MAJOR}.${PYTHON_MINOR}"

if [ "$PYTHON_MAJOR" -lt "3" ] || { [ "$PYTHON_MAJOR" -eq "3" ] && [ "$PYTHON_MINOR" -lt "9" ]; }; then
    echo "⚠️  ERROR: Python ${PYTHON_VERSION} detected."
    echo "   aspose-cad requires Python >= 3.9."
    echo "   Please upgrade to Python 3.9 or later."
    exit 1
fi

echo "Setting up virtual environment for Aspose.CAD MCP Server..."
echo "Platform: cross-platform (Windows x32/x64, Linux, macOS)"
echo "Python version: ${PYTHON_VERSION} ✓"
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
echo "  source servers/cad/.venv/bin/activate"
echo ""
echo "To start the server (stdio):"
echo "  python servers/cad/server.py"
echo ""
echo "To start the server (HTTP on port 8008):"
echo "  python servers/cad/server.py --transport streamable-http --port 8008"
