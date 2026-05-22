@echo off
SET SCRIPT_DIR=%~dp0
SET VENV_DIR=%SCRIPT_DIR%.venv

echo Setting up virtual environment for Aspose.Page MCP Server...
echo (Windows only - aspose-page has no Linux/macOS wheels)

python -m venv "%VENV_DIR%"
call "%VENV_DIR%\Scripts\activate.bat"
pip install --upgrade pip --quiet
pip install -r "%SCRIPT_DIR%requirements.txt" --quiet

echo.
echo Setup complete!
echo To activate: servers\page\.venv\Scripts\activate.bat
echo To start:    python servers\page\server.py
echo HTTP mode:   python servers\page\server.py --transport streamable-http --port 8005
