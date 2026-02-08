#!/bin/bash

# University Admissions Chatbot - Linux/Mac Startup Script

echo "============================================================"
echo "   UNIVERSITY ADMISSIONS CHATBOT - STARTUP"
echo "============================================================"
echo ""

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "[ERROR] .env file not found!"
    echo ""
    echo "Please create .env file from .env.example:"
    echo "  1. Copy .env.example to .env"
    echo "  2. Add your GEMINI_API_KEY and SCALEDOWN_API_KEY"
    echo ""
    echo "Example:"
    echo "  cp .env.example .env"
    echo "  nano .env"
    echo ""
    exit 1
fi

echo "[1/3] Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python 3 not found! Please install Python 3.8+"
    echo "Download from: https://python.org"
    exit 1
fi
python3 --version

echo ""
echo "[2/3] Checking dependencies..."
cd backend
if ! python3 -c "import flask" &> /dev/null; then
    echo "[WARNING] Dependencies not installed!"
    echo "Installing required packages..."
    pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "[ERROR] Failed to install dependencies"
        exit 1
    fi
fi
echo "Dependencies OK"

echo ""
echo "[3/3] Starting Flask backend server..."
echo "------------------------------------------------------------"
echo "Backend will start on http://localhost:5000"
echo ""
echo "INSTRUCTIONS:"
echo "  1. Keep this terminal open (backend server)"
echo "  2. Open frontend/index.html in your browser"
echo "  3. Start chatting!"
echo ""
echo "Press Ctrl+C to stop the server"
echo "============================================================"
echo ""

python3 app.py
