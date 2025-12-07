@echo off
REM gitbro - AI-Powered Git CLI Tool (Windows)

setlocal

set "SCRIPT_DIR=%~dp0"
set "PROJECT_ROOT=%SCRIPT_DIR%.."
set "VENV_PATH=%PROJECT_ROOT%\venv"

REM Activate virtual environment if exists
if exist "%VENV_PATH%\Scripts\activate.bat" (
    call "%VENV_PATH%\Scripts\activate.bat"
)

python "%PROJECT_ROOT%\src\cli.py" %*

