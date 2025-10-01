@echo off
setlocal

set "ROOT=%~dp0"
set "VENV=%ROOT%..\.venv"

if exist "%VENV%\Scripts\activate.bat" (
    call "%VENV%\Scripts\activate.bat"
)

cd /d "%ROOT%"
python "Snake Game.py"

endlocal
