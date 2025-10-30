@echo off
cls
echo.
echo ========================================
echo   Open Web Test Page
echo ========================================
echo.
echo Opening browser...
echo.

start http://localhost:8000/test

echo.
echo Done!
echo.
echo Note: Server must be running first
echo       Run: START-SERVER.bat
echo.
pause
