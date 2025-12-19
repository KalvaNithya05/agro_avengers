@echo off
echo ===================================================
echo   Starting Mitti Mitra System...
echo ===================================================

echo 1. Starting Backend (Port 5000)...
start "Mitti Mitra Backend" cmd /k "cd /d %~dp0 && python backend/app.py"

echo 2. Starting Frontend (Port 5173)...
start "Mitti Mitra Frontend" cmd /k "cd /d %~dp0\frontend && npm run dev"

echo 3. Starting Raspberry Pi Collector (Mock Mode)...
start "Mitti Mitra Pi Collector" cmd /k "cd /d %~dp0 && python raspberry_pi/main.py"

echo ===================================================
echo   All systems launched!
echo ===================================================
echo   Frontend: http://localhost:5173
echo   Backend:  http://localhost:5000
echo ===================================================
pause
