@echo off
:: Setup virtual environment for Aspose Words standalone MCP server

SET SCRIPT_DIR=%~dp0
SET VENV_DIR=%SCRIPT_DIR%.venv

echo Setting up virtual environment for Aspose.Words MCP Server...
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
echo   servers\words\.venv\Scripts\activate.bat
echo.
echo To start the server:
echo   servers\words\.venv\Scripts\python.exe servers\words\server.py
