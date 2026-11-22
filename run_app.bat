@echo off
setlocal
cd /d "%~dp0"

if exist ".venv\Scripts\python.exe" (
    set "PYTHON=.venv\Scripts\python.exe"
) else (
    where py >nul 2>nul
    if not errorlevel 1 (
        set "PYTHON=py"
    ) else (
        set "PYTHON=python"
    )
)

"%PYTHON%" -c "import pypdf" >nul 2>nul
if errorlevel 1 (
    echo Installing dependencies...
    "%PYTHON%" -m pip install -r requirements.txt
    if errorlevel 1 (
        echo Failed to install dependencies.
        pause
        exit /b 1
    )
)

"%PYTHON%" src\main.py
if errorlevel 1 (
    echo.
    echo Application exited with an error.
    pause
)
