@echo off
cls
echo.
echo ========================================
echo   Sentiment Analysis Server
echo ========================================
echo.
echo Server URL: http://localhost:8000
echo Web Test:   http://localhost:8000/test
echo API Docs:   http://localhost:8000/docs
echo.
echo Note: If port 8000 is already in use,
echo       run KILL-SERVER.bat first
echo.
echo ========================================
echo.

cd /d "%~dp0\src"
python main.py

echo.
pause
