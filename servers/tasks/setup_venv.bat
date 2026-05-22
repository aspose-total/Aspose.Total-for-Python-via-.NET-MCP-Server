@echo off
SET SCRIPT_DIR=%~dp0
SET VENV_DIR=%SCRIPT_DIR%.venv

echo Setting up virtual environment for Aspose.Tasks MCP Server...
echo Platform: cross-platform (Windows x32/x64, Linux, macOS)

python -m venv "%VENV_DIR%"
call "%VENV_DIR%\Scripts\activate.bat"

echo Installing dependencies...
pip install --upgrade pip --quiet
pip install -r "%SCRIPT_DIR%requirements.txt" --quiet

echo.
echo Setup complete!
echo To activate:   servers\tasks\.venv\Scripts\activate.bat
echo To start:      python servers\tasks\server.py
echo HTTP mode:     python servers\tasks\server.py --transport streamable-http --port 8009
