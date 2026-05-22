@echo off
SET SCRIPT_DIR=%~dp0
SET VENV_DIR=%SCRIPT_DIR%.venv

echo Setting up virtual environment for Aspose.Diagram MCP Server...
echo Platform: cross-platform (Windows, Linux, macOS)
echo.
echo PACKAGE NOTE: Installing aspose-diagram-python (with -python suffix)
echo   NOT aspose-diagram       -- that is the Java/JPype variant requiring a JVM
echo   NOT aspose-diagram-cloud -- that requires cloud API credentials
echo.

python -m venv "%VENV_DIR%"
call "%VENV_DIR%\Scripts\activate.bat"

echo Installing dependencies...
pip install --upgrade pip --quiet
pip install -r "%SCRIPT_DIR%requirements.txt" --quiet

echo.
echo Setup complete!
echo To activate:   servers\diagram\.venv\Scripts\activate.bat
echo To start:      python servers\diagram\server.py
echo HTTP mode:     python servers\diagram\server.py --transport streamable-http --port 8010
