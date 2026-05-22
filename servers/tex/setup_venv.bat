@echo off
:: Setup virtual environment for Aspose TeX standalone MCP server
:: PLATFORM: Windows only (aspose-tex-net has no Linux/macOS wheels)

SET SCRIPT_DIR=%~dp0
SET VENV_DIR=%SCRIPT_DIR%.venv

echo Setting up virtual environment for Aspose.TeX MCP Server...
echo (Windows only - aspose-tex-net has no Linux/macOS wheels)
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
echo   servers\tex\.venv\Scripts\activate.bat
echo.
echo To start the server (stdio):
echo   python servers\tex\server.py
echo.
echo To start the server (HTTP):
echo   python servers\tex\server.py --transport streamable-http --port 8002
