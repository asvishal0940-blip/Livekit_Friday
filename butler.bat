@echo off
REM Butler Mode - Windows Batch Wrapper
REM Usage: butler [command] [args...]

setlocal enabledelayedexpansion

REM Get the directory where this script is located
set BUTLER_DIR=%~dp0
set VENV_PYTHON=%BUTLER_DIR%venv\Scripts\python.exe

REM Run butler.py with all arguments
%VENV_PYTHON% "%BUTLER_DIR%butler.py" %*

endlocal
