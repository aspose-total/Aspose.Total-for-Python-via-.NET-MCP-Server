@echo off
SET SCRIPT_DIR=%~dp0
SET VENV_DIR=%SCRIPT_DIR%.venv

echo Setting up virtual environment for Aspose.CAD MCP Server...
echo Platform: cross-platform (Windows x32/x64, Linux, macOS)
echo NOTE: aspose-cad requires Python ^>=3.9

python -m venv "%VENV_DIR%"
call "%VENV_DIR%\Scripts\activate.bat"

echo Installing dependencies...
pip install --upgrade pip --quiet
pip install -r "%SCRIPT_DIR%requirements.txt" --quiet

echo.
echo Setup complete!
echo To activate:   servers\cad\.venv\Scripts\activate.bat
echo To start:      python servers\cad\server.py
echo HTTP mode:     python servers\cad\server.py --transport streamable-http --port 8008
