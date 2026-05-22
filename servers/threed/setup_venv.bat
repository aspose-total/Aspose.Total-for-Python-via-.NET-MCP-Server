@echo off
SET SCRIPT_DIR=%~dp0
SET VENV_DIR=%SCRIPT_DIR%.venv

echo Setting up virtual environment for Aspose.3D MCP Server...
echo Platform: cross-platform (Windows, Linux, macOS)
echo Package: aspose-3d (Python module: aspose.threed)

python -m venv "%VENV_DIR%"
call "%VENV_DIR%\Scripts\activate.bat"

echo Installing dependencies...
pip install --upgrade pip --quiet
pip install -r "%SCRIPT_DIR%requirements.txt" --quiet

echo.
echo Setup complete!
echo To activate:   servers\threed\.venv\Scripts\activate.bat
echo To start:      python servers\threed\server.py
echo HTTP mode:     python servers\threed\server.py --transport streamable-http --port 8007
