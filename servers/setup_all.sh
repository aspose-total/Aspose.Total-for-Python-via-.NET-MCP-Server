#!/usr/bin/env bash
# Setup all Aspose MCP server virtual environments.
# Run from the servers/ folder — each product gets its own isolated .venv.
# Usage:  bash setup_all.sh
#         bash setup_all.sh ocr words pdf    <- install specific products only
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FAILED=()

# If specific products are passed as arguments, use those; otherwise install all.
if [ $# -eq 0 ]; then
    PRODUCTS=(barcode cad cells diagram email finance html imaging ocr page pdf psd slides svg tasks tex threed words zip)
else
    PRODUCTS=("$@")
fi

echo ""
echo "============================================================"
echo " Aspose MCP Servers — Setup All"
echo "============================================================"
echo " Products: ${PRODUCTS[*]}"
echo "============================================================"
echo ""

for PRODUCT in "${PRODUCTS[@]}"; do
    SETUP_SCRIPT="${SCRIPT_DIR}/${PRODUCT}/setup_venv.sh"
    if [ ! -f "${SETUP_SCRIPT}" ]; then
        echo "[SKIP] ${PRODUCT} — setup_venv.sh not found at ${SETUP_SCRIPT}"
        echo ""
        continue
    fi

    echo "------------------------------------------------------------"
    echo " Setting up: ${PRODUCT}"
    echo "------------------------------------------------------------"
    if bash "${SETUP_SCRIPT}"; then
        echo "[OK]   ${PRODUCT}"
    else
        echo "[FAIL] ${PRODUCT} setup failed."
        FAILED+=("${PRODUCT}")
    fi
    echo ""
done

echo "============================================================"
if [ ${#FAILED[@]} -eq 0 ]; then
    echo " All servers set up successfully."
else
    echo " Completed with failures:"
    for F in "${FAILED[@]}"; do
        echo "   - ${F}"
    done
    echo " Re-run setup_venv.sh inside each failed server folder"
    echo " to see the full error output."
fi
echo "============================================================"
echo ""
