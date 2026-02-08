# Installation Guide

## Prerequisites

Before you begin, ensure you have the following installed:

### Required Software

1. **Python 3.8 or higher**
   ```bash
   python --version  # Should be 3.8+
   ```

2. **pip** (Python package manager)
   ```bash
   pip --version
   ```

3. **Git** (for cloning the repository)
   ```bash
   git --version
   ```

4. **Web Browser** (Chrome, Firefox, Safari, or Edge)

### Required API Keys

You'll need the following API keys:

1. **Google Gemini API Key**
   - Sign up at: https://makersuite.google.com/app/apikey
   - Free tier available
   - Required for AI responses

2. **Scaledown API Key**
   - Sign up at: https://scaledown.xyz
   - Free tier available
   - Required for context compression

---

## Installation Steps

### Step 1: Clone the Repository

```bash
# Clone the repository
git clone <your-repository-url>

# Navigate to project directory
cd UAC
```

### Step 2: Set Up Python Environment

#### Option A: Using Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

#### Option B: System-wide Installation

```bash
# Install directly to system Python
# (Not recommended for development)
pip install -r requirements.txt
```

### Step 3: Install Dependencies

```bash
# Install all required packages
pip install -r requirements.txt

# Verify installation
pip list
```

**Expected packages:**
- Flask (3.0.0)
- flask-cors (4.0.0)
- google-generativeai (latest)
- python-dotenv (1.0.0)
- requests (2.31.0)
- beautifulsoup4 (4.12.0)
- pdfplumber (0.10.0)
- PyPDF2 (3.0.0)

### Step 4: Configure Environment Variables

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env file with your API keys
# On Windows:
notepad .env

# On macOS/Linux:
nano .env
# or
vim .env
```

**Required configuration in `.env`:**

```bash
# ========================================
# API Keys (REQUIRED)
# ========================================
GEMINI_API_KEY=your_gemini_api_key_here
SCALEDOWN_API_KEY=your_scaledown_api_key_here

# ========================================
# Flask Configuration
# ========================================
FLASK_ENV=development
FLASK_DEBUG=True
FLASK_PORT=5000
FLASK_HOST=0.0.0.0

# ========================================
# Gemini Settings
# ========================================
GEMINI_MODEL=gemini-2.5-flash
GEMINI_TEMPERATURE=0.7
GEMINI_MAX_TOKENS=1024
GEMINI_TOP_P=0.95

# ========================================
# Scaledown Settings
# ========================================
SCALEDOWN_RATE=auto
SCALEDOWN_MODEL=gemini-2.5-flash

# ========================================
# Data Paths
# ========================================
COLLEGE_DATA_DIR=college_data
CACHE_DIR=cache
LOG_DIR=logs

# ========================================
# Optional Settings
# ========================================
SCRAPING_ENABLED=False
CACHE_TTL=3600
LOG_LEVEL=INFO
```

### Step 5: Verify Installation

```bash
# Run the system check script
python check_system.py
```

**Expected output:**
```
✓ Python version: 3.8+
✓ All dependencies installed
✓ .env file configured
✓ API keys present
✓ Directories created
✓ Data files found
```

---

## Starting the Application

### Method 1: Using Start Scripts (Recommended)

#### Windows:
```bash
start.bat
```

#### macOS/Linux:
```bash
chmod +x start.sh
./start.sh
```

### Method 2: Manual Start

#### Terminal 1 - Backend:
```bash
# Navigate to backend directory
cd backend

# Start Flask server
python app.py
```

**Expected output:**
```
============================================================
UNIVERSITY ADMISSIONS CHATBOT - STARTING
============================================================

[OK] Configuration validated
[OK] Context loaded successfully
   Size: 60125 characters

============================================================
SERVER READY
============================================================
Listening on http://0.0.0.0:5000
Press CTRL+C to stop
```

#### Browser - Frontend:
```bash
# Option 1: Open directly in browser
# Navigate to: file:///path/to/UAC/frontend/index.html

# Option 2: Use local server (recommended for testing)
cd frontend
python -m http.server 8000
# Then open: http://localhost:8000
```

---

## Verification

### 1. Backend Health Check

Open in browser or use curl:

```bash
# Browser:
http://localhost:5000/health

# Curl:
curl http://localhost:5000/health
```

**Expected response:**
```json
{
  "status": "healthy",
  "context_loaded": true,
  "context_size": 60125,
  "gemini_configured": true,
  "scaledown_configured": true
}
```

### 2. Frontend Test

1. Open `frontend/index.html` in your browser
2. You should see:
   - Material Design interface
   - Welcome message from bot
   - Input field at bottom
   - Quick action chips (Requirements, Programs, Tuition, Deadlines)

3. Test a query:
   - Type: "What programs do you offer?"
   - Click Send or press Enter
   - Wait for response (first query: 15-20s, subsequent: 2-5s)

### 3. Test Chatbot Functionality

**Try these queries:**

1. "When was the university established?"
   - Expected: "1996"

2. "What is the BCA fee?"
   - Expected: "INR 5,70,000 for 3 years"

3. "What are the B.Tech specializations?"
   - Expected: List of specializations (CSE, AI & ML, etc.)

4. "What is the admission deadline?"
   - Expected: "31 March 2026 (regular deadline)"

---

## Troubleshooting Installation

### Issue: ModuleNotFoundError

**Symptom:**
```
ModuleNotFoundError: No module named 'flask'
```

**Solution:**
```bash
# Ensure virtual environment is activated
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Issue: API Key Not Found

**Symptom:**
```
GEMINI_API_KEY is not set in environment variables
```

**Solution:**
```bash
# Check .env file exists
ls -la | grep .env

# Verify .env content
cat .env

# Ensure proper format (no quotes needed):
GEMINI_API_KEY=AIza...
SCALEDOWN_API_KEY=sk_...
```

### Issue: Port Already in Use

**Symptom:**
```
OSError: [Errno 98] Address already in use
```

**Solution:**
```bash
# Option 1: Kill process on port 5000
# On Windows:
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# On macOS/Linux:
lsof -i :5000
kill -9 <PID>

# Option 2: Use different port
FLASK_PORT=5001 python backend/app.py
```

### Issue: CORS Errors in Browser

**Symptom:**
```
Access to fetch at 'http://localhost:5000/chat' from origin 'null' has been blocked by CORS policy
```

**Solution:**
```bash
# Ensure flask-cors is installed
pip install flask-cors

# Or serve frontend via HTTP server
cd frontend
python -m http.server 8000
# Open: http://localhost:8000
```

### Issue: Data Files Not Found

**Symptom:**
```
College data directory does not exist: college_data
```

**Solution:**
```bash
# Verify directory structure
ls -la college_data/

# Should contain:
# - admissions.txt
# - programs.txt
# - fees.txt

# If missing, restore from repository
git checkout college_data/
```

### Issue: Slow First Response

**This is normal:**
- First query: ~15-20 seconds (includes compression)
- Subsequent queries: ~2-5 seconds (uses cache)

**To speed up:**
- Compression is cached after first use
- Refresh browser only when needed (clears cache)

---

## Directory Setup Verification

Run this command to verify directory structure:

```bash
tree -L 2 -I 'venv|__pycache__|*.pyc|.git'
```

**Expected structure:**
```
UAC/
├── backend/
│   ├── app.py
│   ├── config.py
│   ├── gemini_client.py
│   ├── ingest.py
│   ├── scaledown.py
│   └── utils.py
├── frontend/
│   ├── index.html
│   ├── script.js
│   └── style.css
├── college_data/
│   ├── admissions.txt
│   ├── fees.txt
│   └── programs.txt
├── docs/
│   └── (documentation files)
├── cache/         # Auto-created
├── logs/          # Auto-created
├── .env
├── .env.example
├── .gitignore
├── requirements.txt
├── README.md
├── start.bat
└── start.sh
```

---

## Post-Installation Checklist

- [ ] Python 3.8+ installed
- [ ] Dependencies installed (pip install -r requirements.txt)
- [ ] .env file configured with API keys
- [ ] Backend starts without errors
- [ ] Health check returns 200 OK
- [ ] Frontend displays correctly
- [ ] Test query returns response
- [ ] Compression stats showing (first query)
- [ ] Second query is faster (cache working)

---

## Next Steps

After successful installation:

1. **Read the Documentation**
   - [Architecture Overview](ARCHITECTURE.md)
   - [API Reference](API_REFERENCE.md)
   - [Configuration Guide](CONFIGURATION.md)

2. **Customize Your Data**
   - Edit `college_data/*.txt` files
   - Reload context: `POST http://localhost:5000/reload-context`

3. **Development**
   - See [Development Guide](DEVELOPMENT.md)
   - Set up your IDE
   - Review coding standards

4. **Deployment**
   - See [Deployment Guide](DEPLOYMENT.md)
   - Production configuration
   - Server setup

---

## Getting Help

If you encounter issues:

1. Check [Troubleshooting Guide](TROUBLESHOOTING.md)
2. Review error logs in `logs/chatbot.log`
3. Run `python check_system.py` for diagnostics
4. Create a GitHub issue with:
   - Error message
   - Steps to reproduce
   - System information (OS, Python version)
   - Log output

---

**Installation complete! 🎉**

Your University Admissions Chatbot is now ready to use.
