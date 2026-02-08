# Troubleshooting Guide

Common issues and their solutions for the University Admissions Chatbot.

## Table of Contents

1. [Installation Issues](#installation-issues)
2. [Backend Issues](#backend-issues)
3. [Frontend Issues](#frontend-issues)
4. [API Issues](#api-issues)
5. [Performance Issues](#performance-issues)
6. [Data Issues](#data-issues)
7. [Deployment Issues](#deployment-issues)

---

## Installation Issues

### Python Version Incompatible

**Symptom:**
```
ERROR: This package requires Python 3.8 or higher
```

**Solution:**
```bash
# Check Python version
python --version

# If < 3.8, install newer Python
# Windows: Download from python.org
# macOS: brew install python@3.11
# Linux: sudo apt-get install python3.11

# Use specific version
python3.11 -m venv venv
```

### Module Not Found

**Symptom:**
```
ModuleNotFoundError: No module named 'flask'
```

**Solution:**
```bash
# 1. Activate virtual environment
# Windows:
venv\Scripts\activate

# macOS/Linux:
source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Verify installation
pip list | grep flask
```

### Permission Denied

**Symptom:**
```
PermissionError: [Errno 13] Permission denied: 'logs'
```

**Solution:**
```bash
# Fix directory permissions
chmod -R 755 logs cache

# Or run with sudo (not recommended)
sudo python backend/app.py
```

### requirements.txt Not Found

**Symptom:**
```
ERROR: Could not open requirements file: No such file or directory
```

**Solution:**
```bash
# Ensure you're in project root
cd path/to/UAC

# Verify file exists
ls requirements.txt

# If missing, recreate:
cat > requirements.txt <<EOF
Flask==3.0.0
flask-cors==4.0.0
google-generativeai
python-dotenv==1.0.0
requests==2.31.0
beautifulsoup4==4.12.0
pdfplumber==0.10.0
PyPDF2==3.0.0
EOF
```

---

## Backend Issues

### API Key Not Found

**Symptom:**
```
GEMINI_API_KEY is not set in environment variables
```

**Solution:**
```bash
# 1. Check .env exists
ls -la .env

# 2. Verify content
cat .env | grep GEMINI_API_KEY

# 3. Correct format (NO quotes):
# CORRECT:
GEMINI_API_KEY=AIzaSyXXXXXX

# INCORRECT:
GEMINI_API_KEY="AIzaSyXXXXXX"

# 4. Restart backend
python backend/app.py
```

### Port Already in Use

**Symptom:**
```
OSError: [Errno 98] Address already in use
```

**Solution:**
```bash
# Find process using port 5000
# Windows:
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# macOS/Linux:
lsof -i :5000
kill -9 <PID>

# Or use different port
FLASK_PORT=5001 python backend/app.py
```

### Context Not Loading

**Symptom:**
```
ERROR: No context available
```

**Solution:**
```bash
# 1. Verify data files exist
ls -la college_data/

# Should see:
# - admissions.txt
# - programs.txt
# - fees.txt

# 2. Check file permissions
chmod 644 college_data/*.txt

# 3. Reload context
curl -X POST http://localhost:5000/reload-context

# 4. Check logs
cat logs/chatbot.log | grep ERROR
```

### Scaledown API Timeout

**Symptom:**
```
Scaledown API timeout after 15s
```

**Solution:**
```bash
# 1. Check Scaledown API key
echo $SCALEDOWN_API_KEY

# 2. Test API directly
curl -X POST https://api.scaledown.xyz/compress/raw/ \
  -H "x-api-key: $SCALEDOWN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"context": "test", "prompt": "test", "model": "gemini-2.5-flash"}'

# 3. If timeout persists, increase timeout in config.py:
SCALEDOWN_TIMEOUT = 30  # Increase from 15

# 4. Or disable compression (fallback mode)
# Remove SCALEDOWN_API_KEY from .env
```

### Gemini API Error

**Symptom:**
```
GEMINI_ERROR: Failed to generate response
```

**Solutions:**

**A. Invalid API Key:**
```bash
# Test Gemini API key
python - <<EOF
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
model = genai.GenerativeModel('gemini-2.5-flash')
response = model.generate_content('Hello')
print(response.text)
EOF
```

**B. Rate Limit Exceeded:**
```
# Wait 1 minute and retry
# Or upgrade to paid tier at https://ai.google.dev
```

**C. Model Not Available:**
```python
# Try different model in .env
GEMINI_MODEL=gemini-pro
```

---

## Frontend Issues

### CORS Error

**Symptom:**
```
Access to fetch at 'http://localhost:5000/chat' has been blocked by CORS policy
```

**Solution:**

**Option 1: Serve frontend via HTTP server**
```bash
cd frontend
python -m http.server 8000

# Open: http://localhost:8000
# (Not file://...)
```

**Option 2: Verify flask-cors installed**
```bash
pip install flask-cors

# Check in backend/app.py:
from flask_cors import CORS
CORS(app)
```

**Option 3: Allow file:// origin (temporary)**
```python
# In backend/app.py
CORS(app, resources={
    r"/*": {
        "origins": ["null", "http://localhost:*"]
    }
})
```

### Cannot Connect to Server

**Symptom:**
```
Failed to fetch: Cannot connect to server
```

**Solutions:**

**A. Backend not running:**
```bash
# Start backend
python backend/app.py

# Verify running
curl http://localhost:5000/health
```

**B. Wrong URL:**
```javascript
// Check frontend/script.js CONFIG.API_BASE_URL
const CONFIG = {
    API_BASE_URL: 'http://localhost:5000',  // Correct
    // NOT: 'http://localhost:5001'
};
```

**C. Firewall blocking:**
```bash
# Windows: Allow Python in firewall
# macOS: System Preferences > Security > Firewall
# Linux: sudo ufw allow 5000
```

### Typing Indicator Stuck

**Symptom:**
Typing indicator shows indefinitely without response

**Solutions:**

**A. Request timeout too short:**
```javascript
// In frontend/script.js, increase timeout
CONFIG.REQUEST_TIMEOUT = 60000  // 60 seconds (from 45)
```

**B. Backend crashed:**
```bash
# Check backend logs
cat logs/chatbot.log | tail -50

# Restart backend
python backend/app.py
```

**C. Clear browser cache:**
```
1. Open DevTools (F12)
2. Right-click refresh button
3. Select "Empty Cache and Hard Reload"
```

### Messages Not Displaying

**Symptom:**
Messages sent but not showing in chat window

**Solutions:**

**A. Check browser console:**
```
1. Open DevTools (F12)
2. Check Console tab for JavaScript errors
3. Fix any errors shown
```

**B. Verify element IDs:**
```html
<!-- In frontend/index.html, ensure these exist: -->
<div id="messages"></div>
<input id="userInput" />
<button id="sendBtn"></button>
```

**C. Clear localStorage:**
```javascript
// In browser console
localStorage.clear();
location.reload();
```

---

## API Issues

### 400 Bad Request

**Symptom:**
```json
{
  "error": true,
  "error_code": "INVALID_JSON",
  "message": "Invalid JSON request"
}
```

**Solution:**
```bash
# Ensure proper JSON format
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \  # Required header
  -d '{"message": "test"}'  # Valid JSON
```

### 500 Internal Server Error

**Symptom:**
```json
{
  "error": true,
  "error_code": "INTERNAL_ERROR"
}
```

**Solutions:**

**A. Check backend logs:**
```bash
cat logs/chatbot.log | grep ERROR | tail -20
```

**B. Enable debug mode:**
```bash
# In .env
FLASK_DEBUG=True

# Restart backend
# Error details will show in console
```

**C. Test individual components:**
```python
# Test context loading
from backend.ingest import load_local_data
result = load_local_data('college_data')
print(result)

# Test Gemini
from backend.gemini_client import GeminiClient
client = GeminiClient()
response = client.generate_response("Test", "Test query", [])
print(response)
```

### Slow Response Times

**Symptom:**
Every request takes 15-20 seconds

**Solutions:**

**A. Verify caching working:**
```bash
# First request should be ~15-20s
# Second request should be ~2-5s

# Check logs for "Using cached compressed context"
cat logs/chatbot.log | grep cached
```

**B. Clear and rebuild cache:**
```bash
# Stop backend
# Delete cache
rm -rf cache/*

# Restart backend
python backend/app.py
```

**C. Reduce timeout:**
```python
# In backend/config.py
SCALEDOWN_TIMEOUT = 10  # From 15

# In frontend/script.js
CONFIG.REQUEST_TIMEOUT = 30000  # From 45000
```

---

## Performance Issues

### High Memory Usage

**Symptom:**
Backend consuming > 500MB RAM

**Solutions:**

**A. Limit context size:**
```python
# In backend/ingest.py
def load_local_data():
    # Limit file size
    max_size = 50000  # 50KB per file
    ...
```

**B. Clear cache periodically:**
```bash
# Add to crontab (Linux/macOS)
0 */6 * * * rm -rf /path/to/UAC/cache/*

# Windows Task Scheduler
# del C:\path\to\UAC\cache\* /Q
```

**C. Reduce conversation history:**
```python
# In backend/gemini_client.py
# Keep only last 3 exchanges (instead of 5)
conversation_history = conversation_history[-3:]
```

### High CPU Usage

**Symptom:**
Backend using 100% CPU constantly

**Solutions:**

**A. Use production server:**
```bash
# Install gunicorn
pip install gunicorn

# Run with multiple workers
gunicorn -w 2 -b 0.0.0.0:5000 backend.app:app
```

**B. Add request throttling:**
```python
# In backend/app.py
from flask_limiter import Limiter

limiter = Limiter(app, default_limits=["100 per hour"])
```

**C. Profile the application:**
```bash
pip install py-spy

# Profile running backend
py-spy top --pid <backend_pid>
```

### Slow File Loading

**Symptom:**
Context loading takes > 5 seconds

**Solutions:**

**A. Optimize file reading:**
```python
# Use buffered reading
with open(file, 'r', buffering=8192) as f:
    content = f.read()
```

**B. Pre-compile context:**
```bash
# Create single merged file
cat college_data/*.txt > college_data/merged.txt

# Load only merged file
```

**C. Use SSD instead of HDD**
- Move project to SSD if on HDD

---

## Data Issues

### Encoding Errors

**Symptom:**
```
UnicodeDecodeError: 'utf-8' codec can't decode byte
```

**Solution:**
```python
# In backend/ingest.py, fallback encodings already implemented:
encodings = ['utf-8', 'latin-1', 'cp1252']

# Or convert files to UTF-8:
iconv -f ISO-8859-1 -t UTF-8 input.txt > output.txt
```

### Missing Data Files

**Symptom:**
```
FileNotFoundError: [Errno 2] No such file or directory: 'college_data/admissions.txt'
```

**Solution:**
```bash
# Restore from Git
git checkout college_data/

# Or create minimal file
cat > college_data/admissions.txt <<EOF
University Name: Sample University
Established: 2000
Location: Sample City, Sample State
EOF
```

### Outdated Information

**Symptom:**
Chatbot provides old information after data update

**Solution:**
```bash
# Option 1: Reload context
curl -X POST http://localhost:5000/reload-context

# Option 2: Restart backend
# Stop (Ctrl+C) and restart:
python backend/app.py

# Verify new data loaded
curl http://localhost:5000/health
# Check context_size changed
```

---

## Deployment Issues

### Production Server Won't Start

**Symptom:**
```
gunicorn: command not found
```

**Solution:**
```bash
# Install gunicorn
pip install gunicorn

# Test locally first
gunicorn -w 1 -b 127.0.0.1:5000 backend.app:app

# If works, deploy:
gunicorn -w 4 -b 0.0.0.0:80 backend.app:app
```

### SSL Certificate Errors

**Symptom:**
```
SSL: CERTIFICATE_VERIFY_FAILED
```

**Solutions:**

**A. Update certificates:**
```bash
# macOS:
/Applications/Python\ 3.11/Install\ Certificates.command

# Linux:
sudo apt-get install ca-certificates
sudo update-ca-certificates
```

**B. Use certifi:**
```bash
pip install certifi

# In Python code:
import certifi
requests.get(url, verify=certifi.where())
```

### Environment Variables Not Loading

**Symptom:**
API keys work locally but not in production

**Solutions:**

**A. System environment variables:**
```bash
# Linux/macOS: Add to ~/.bashrc or /etc/environment
export GEMINI_API_KEY=AIza...
export SCALEDOWN_API_KEY=sk_...

# Reload:
source ~/.bashrc
```

**B. systemd service file:**
```ini
# /etc/systemd/system/chatbot.service
[Service]
Environment="GEMINI_API_KEY=AIza..."
Environment="SCALEDOWN_API_KEY=sk..."
```

**C. Docker .env file:**
```bash
# Ensure .env mounted or variables passed:
docker run -e GEMINI_API_KEY=$GEMINI_API_KEY ...
```

---

## Debugging Tools

### Health Check

```bash
# Check server status
curl http://localhost:5000/health | jq

# Expected output:
# {
#   "status": "healthy",
#   "context_loaded": true,
#   "gemini_configured": true,
#   "scaledown_configured": true
# }
```

### Log Analysis

```bash
# Show all errors
cat logs/chatbot.log | grep ERROR

# Show last 50 lines
tail -50 logs/chatbot.log

# Follow logs in real-time
tail -f logs/chatbot.log

# Search for specific query
cat logs/chatbot.log | grep "What programs"
```

### Test Scripts

```bash
# System check
python check_system.py

# Backend test
python test_system.py

# API test
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "test"}'
```

### Browser DevTools

```
1. Open DevTools (F12)
2. Network tab - Check API requests/responses
3. Console tab - Check JavaScript errors
4. Application tab - Check localStorage
```

---

## Getting Help

If issue persists:

1. **Check Documentation:**
   - [Installation Guide](INSTALLATION.md)
   - [Configuration Guide](CONFIGURATION.md)
   - [API Reference](API_REFERENCE.md)

2. **Review Logs:**
   ```bash
   cat logs/chatbot.log | grep ERROR
   ```

3. **Create GitHub Issue:**
   - Include error message
   - Steps to reproduce
   - System info (OS, Python version)
   - Log excerpt

4. **Community Support:**
   - Check existing issues
   - Search documentation
   - Contact maintainers

---

## Common Error Messages Reference

| Error Message | Likely Cause | Solution |
|---------------|--------------|----------|
| `ModuleNotFoundError` | Missing package | `pip install -r requirements.txt` |
| `API key not set` | Missing .env | Create .env with API keys |
| `Address already in use` | Port conflict | Kill process or use different port |
| `CORS policy` | Origin mismatch | Serve frontend via HTTP server |
| `Context not loaded` | Missing data files | Restore college_data/ |
| `Timeout exceeded` | Slow API | Increase timeout values |
| `JSON decode error` | Invalid response | Check API credentials |
| `Permission denied` | File permissions | `chmod` directories |

---

For detailed configuration and architecture information:
- [Architecture Overview](ARCHITECTURE.md)
- [Development Guide](DEVELOPMENT.md)
- [Deployment Guide](DEPLOYMENT.md)
