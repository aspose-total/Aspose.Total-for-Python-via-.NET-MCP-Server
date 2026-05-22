#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="${SCRIPT_DIR}/.venv"

echo "⚠️  WARNING: aspose-tex-net is Windows only (x86/x64)."
echo "   This setup will attempt installation, but the plugin will not"
echo "   function on Linux or macOS at runtime."
echo ""
echo "Setting up virtual environment for Aspose.TeX MCP Server..."

python3 -m venv "${VENV_DIR}"
source "${VENV_DIR}/bin/activate"
pip install --upgrade pip --quiet
pip install -r "${SCRIPT_DIR}/requirements.txt" --quiet || {
    echo ""
    echo "⚠️  pip install failed. This is expected on Linux/macOS."
    echo "   aspose-tex-net only has Windows wheels on PyPI."
    echo "   Run this script on a Windows machine, or use the Windows batch script."
    exit 1
}

echo ""
echo "✅ Setup complete!"
echo "   Note: tex_plugin.py tools only work on Windows at runtime."
echo ""
echo "To start the server: python servers/tex/server.py"
