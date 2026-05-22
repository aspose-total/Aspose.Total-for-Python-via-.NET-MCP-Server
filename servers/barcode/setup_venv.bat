@echo off
:: Setup virtual environment for Aspose BarCode standalone MCP server

SET SCRIPT_DIR=%~dp0
SET VENV_DIR=%SCRIPT_DIR%.venv

echo Setting up virtual environment for Aspose.BarCode MCP Server...
echo Location: %VENV_DIR%

python -m venv "%VENV_DIR%"
call "%VENV_DIR%\Scripts\activate.bat"

echo Installing dependencies...
pip install --upgrade pip --quiet
pip install -r "%SCRIPT_DIR%requirements.txt" --quiet

echo.
echo Setup complete!
echo.
echo To activate the venv:
echo   servers\barcode\.venv\Scripts\activate.bat
echo.
echo To start the server (stdio):
echo   python servers\barcode\server.py
echo.
echo To start the server (HTTP):
echo   python servers\barcode\server.py --transport streamable-http --port 8001
