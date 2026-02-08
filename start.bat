@echo off
REM University Admissions Chatbot - Windows Startup Script

echo ============================================================
echo    UNIVERSITY ADMISSIONS CHATBOT - STARTUP
echo ============================================================
echo.

REM Check if .env exists
if not exist ".env" (
    echo [ERROR] .env file not found!
    echo.
    echo Please create .env file from .env.example:
    echo   1. Copy .env.example to .env
    echo   2. Add your GEMINI_API_KEY and SCALEDOWN_API_KEY
    echo.
    echo Example:
    echo   copy .env.example .env
    echo   notepad .env
    echo.
    pause
    exit /b 1
)

echo [1/3] Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found! Please install Python 3.8+
    echo Download from: https://python.org
    pause
    exit /b 1
)
python --version

echo.
echo [2/3] Checking dependencies...
cd backend
pip show flask >nul 2>&1
if %errorlevel% neq 0 (
    echo [WARNING] Dependencies not installed!
    echo Installing required packages...
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to install dependencies
        pause
        exit /b 1
    )
)
echo Dependencies OK

echo.
echo [3/3] Starting Flask backend server...
echo ------------------------------------------------------------
echo Backend will start on http://localhost:5000
echo.
echo INSTRUCTIONS:
echo   1. Keep this window open (backend server)
echo   2. Open frontend\index.html in your browser
echo   3. Start chatting!
echo.
echo Press Ctrl+C to stop the server
echo ============================================================
echo.

python app.py

pause
