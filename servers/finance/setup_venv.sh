#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="${SCRIPT_DIR}/.venv"

# Check Python version — aspose-finance requires Python <3.12
PYTHON_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
PYTHON_MINOR=$(python3 -c "import sys; print(sys.version_info.minor)")
PYTHON_MAJOR=$(python3 -c "import sys; print(sys.version_info.major)")

if [ "$PYTHON_MAJOR" -eq "3" ] && [ "$PYTHON_MINOR" -ge "12" ]; then
    echo "⚠️  WARNING: Python ${PYTHON_VERSION} detected."
    echo "   aspose-finance requires Python >=3.5 and <3.12."
    echo "   Please use Python 3.11 or earlier."
    exit 1
fi

echo "Setting up virtual environment for Aspose.Finance MCP Server..."
echo "Platform: cross-platform (Windows x32/x64, Linux, Unix/macOS)"
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
echo "  source servers/finance/.venv/bin/activate"
echo ""
echo "To start the server (stdio):"
echo "  python servers/finance/server.py"
echo ""
echo "To start the server (HTTP on port 8006):"
echo "  python servers/finance/server.py --transport streamable-http --port 8006"
