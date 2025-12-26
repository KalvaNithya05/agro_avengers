@echo off
echo Starting Mitti Mitra Backend...
echo.

set VENV_PYTHON=backend\venv\Scripts\python.exe

if exist "%VENV_PYTHON%" (
    echo Found virtual environment. Using %VENV_PYTHON%
    set PYTHON_CMD=%VENV_PYTHON%
) else (
    echo Virtual environment not found. Using system Python.
    set PYTHON_CMD=python
)

:: Check for Python
%PYTHON_CMD% --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in PATH.
    pause
    exit /b 1
)

:: Install dependencies
echo Installing/Updating dependencies...
%PYTHON_CMD% -m pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Error: Failed to install dependencies.
    pause
    exit /b 1
)

:: Run the app
echo.
echo Starting Flask Server on Port 5000...
cd backend
..\%PYTHON_CMD% app.py
pause
