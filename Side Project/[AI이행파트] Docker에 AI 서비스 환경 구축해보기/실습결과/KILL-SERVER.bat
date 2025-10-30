@echo off
cls
echo.
echo ========================================
echo   Kill Process on Port 8000
echo ========================================
echo.

for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8000 ^| findstr LISTENING') do (
    echo Killing process PID %%a ...
    taskkill /F /PID %%a
)

echo.
echo Done!
echo.
pause
