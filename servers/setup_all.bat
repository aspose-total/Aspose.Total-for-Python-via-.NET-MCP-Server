@echo off
:: Setup all Aspose MCP server virtual environments.
:: Run from the servers/ folder — each product gets its own isolated .venv.
:: Usage:  setup_all.bat
::         setup_all.bat ocr words pdf    <- install specific products only

SETLOCAL ENABLEDELAYEDEXPANSION

SET SCRIPT_DIR=%~dp0
SET FAILED=

:: If specific products are passed as arguments, use those; otherwise install all.
IF "%~1"=="" (
    SET PRODUCTS=barcode cad cells diagram email finance html imaging ocr page pdf psd slides svg tasks tex threed words zip
) ELSE (
    SET PRODUCTS=%*
)

echo.
echo ============================================================
echo  Aspose MCP Servers — Setup All
echo ============================================================
echo  Products: %PRODUCTS%
echo ============================================================
echo.

FOR %%P IN (%PRODUCTS%) DO (
    SET SETUP_SCRIPT=%SCRIPT_DIR%%%P\setup_venv.bat
    IF NOT EXIST "!SETUP_SCRIPT!" (
        echo [SKIP] %%P — setup_venv.bat not found at !SETUP_SCRIPT!
        echo.
    ) ELSE (
        echo ------------------------------------------------------------
        echo  Setting up: %%P
        echo ------------------------------------------------------------
        call "!SETUP_SCRIPT!"
        IF ERRORLEVEL 1 (
            echo [FAIL] %%P setup failed.
            SET FAILED=!FAILED! %%P
        ) ELSE (
            echo [OK]   %%P
        )
        echo.
    )
)

echo ============================================================
IF "%FAILED%"=="" (
    echo  All servers set up successfully.
) ELSE (
    echo  Completed with failures:
    FOR %%F IN (%FAILED%) DO echo    - %%F
    echo  Re-run setup_venv.bat inside each failed server folder
    echo  to see the full error output.
)
echo ============================================================
echo.
