@echo off
SET SCRIPT_DIR=%~dp0
SET VENV_DIR=%SCRIPT_DIR%.venv

echo Setting up virtual environment for Aspose.Email MCP Server...
echo Platform: cross-platform (Windows, Linux, macOS)
echo.
echo PACKAGE NOTE: Installing aspose-email-for-python-via-net (full long name)
echo   NOT aspose-email-cloud -- that requires Aspose Cloud API credentials
echo   NOT aspose-email       -- that package does not exist as a .NET binding
echo.

python -m venv "%VENV_DIR%"
call "%VENV_DIR%\Scripts\activate.bat"

echo Installing dependencies...
pip install --upgrade pip --quiet
pip install -r "%SCRIPT_DIR%requirements.txt" --quiet

echo.
echo Setup complete!
echo To activate:   servers\email\.venv\Scripts\activate.bat
echo To start:      python servers\email\server.py
echo HTTP mode:     python servers\email\server.py --transport streamable-http --port 8011
