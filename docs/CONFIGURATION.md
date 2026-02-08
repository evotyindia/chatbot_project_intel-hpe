# Configuration Guide

Complete reference for configuring the University Admissions Chatbot.

## Table of Contents

1. [Environment Variables](#environment-variables)
2. [Application Configuration](#application-configuration)
3. [API Configuration](#api-configuration)
4. [Data Configuration](#data-configuration)
5. [Performance Tuning](#performance-tuning)
6. [Security Settings](#security-settings)
7. [Logging Configuration](#logging-configuration)

---

## Environment Variables

All configuration is managed through the `.env` file.

### Creating the .env File

```bash
# Copy the example template
cp .env.example .env

# Edit with your values
nano .env  # or vim, code, notepad, etc.
```

### Required Variables

#### API Keys

```bash
# Google Gemini API Key (REQUIRED)
# Get from: https://makersuite.google.com/app/apikey
GEMINI_API_KEY=AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXX

# Scaledown API Key (REQUIRED)
# Get from: https://scaledown.xyz
SCALEDOWN_API_KEY=sk_XXXXXXXXXXXXXXXXXXXXXXXX
```

**Security Note:** Never commit `.env` to Git. It's included in `.gitignore`.

---

### Flask Configuration

```bash
# Environment: development or production
FLASK_ENV=development

# Debug Mode: True or False
# WARNING: Set to False in production for security
FLASK_DEBUG=True

# Port: Default 5000
FLASK_PORT=5000

# Host: 0.0.0.0 allows external access
# Use 127.0.0.1 for localhost only
FLASK_HOST=0.0.0.0
```

#### Production Settings

```bash
FLASK_ENV=production
FLASK_DEBUG=False
FLASK_HOST=0.0.0.0  # Or your domain's IP
FLASK_PORT=80       # Or 443 for HTTPS
```

---

### Gemini AI Configuration

```bash
# Model: gemini-2.5-flash (recommended for speed)
# Other options: gemini-pro, gemini-1.5-pro
GEMINI_MODEL=gemini-2.5-flash

# Temperature: Controls randomness (0.0 to 1.0)
# 0.7 = Balanced creativity and consistency
# Lower = More deterministic
# Higher = More creative
GEMINI_TEMPERATURE=0.7

# Max Tokens: Maximum response length
# Default: 1024 (suitable for most queries)
# Increase for longer responses
GEMINI_MAX_TOKENS=1024

# Top P: Nucleus sampling parameter (0.0 to 1.0)
# 0.95 = Consider top 95% probable tokens
GEMINI_TOP_P=0.95
```

#### Model Selection Guide

| Model | Speed | Quality | Cost | Use Case |
|-------|-------|---------|------|----------|
| gemini-2.5-flash | ⚡⚡⚡ | ⭐⭐⭐ | $ | Production (recommended) |
| gemini-pro | ⚡⚡ | ⭐⭐⭐⭐ | $$ | High quality needed |
| gemini-1.5-pro | ⚡ | ⭐⭐⭐⭐⭐ | $$$ | Maximum quality |

---

### Scaledown Configuration

```bash
# Compression Rate: 'auto' or specific value (0.1 to 1.0)
# auto = Scaledown decides optimal compression
# 0.5 = Compress to 50% of original size
SCALEDOWN_RATE=auto

# Target Model: Must match Gemini model
SCALEDOWN_MODEL=gemini-2.5-flash
```

---

### Data Paths

```bash
# Directory containing university data TXT files
COLLEGE_DATA_DIR=college_data

# Directory for compression cache
CACHE_DIR=cache

# Directory for log files
LOG_DIR=logs
```

**Note:** Directories are created automatically if they don't exist.

---

### Optional Features

```bash
# Web Scraping: Enable/disable university website scraping
# Default: False (use local files only)
SCRAPING_ENABLED=False

# Cache TTL: Time-to-live for web scrape cache (seconds)
# Default: 3600 (1 hour)
CACHE_TTL=3600

# Logging Level: DEBUG, INFO, WARNING, ERROR, CRITICAL
# Default: INFO
LOG_LEVEL=INFO
```

---

## Application Configuration

### backend/config.py

The main configuration file with hardcoded defaults and environment loading.

#### Key Configuration Sections

**1. Scaledown Timeout**

```python
# Timeout for Scaledown API requests (seconds)
SCALEDOWN_TIMEOUT = 15  # Reduced from 30 for faster failure
```

**2. System Instruction**

```python
SYSTEM_INSTRUCTION = """
You are an intelligent University Admissions Assistant...
# Edit this to customize chatbot behavior
"""
```

**3. CORS Settings**

```python
# CORS Origins: Allowed origins for API access
CORS_ORIGINS = os.getenv('CORS_ORIGINS', '*').split(',')

# Production example:
CORS_ORIGINS=['https://yourdomain.com', 'https://www.yourdomain.com']
```

---

## API Configuration

### Gemini API Settings

Located in `backend/gemini_client.py`:

```python
class GeminiClient:
    def __init__(self):
        self.model = genai.GenerativeModel(
            model_name=GEMINI_MODEL,
            generation_config={
                'temperature': GEMINI_TEMPERATURE,
                'max_output_tokens': GEMINI_MAX_TOKENS,
                'top_p': GEMINI_TOP_P,
            },
            system_instruction=SYSTEM_INSTRUCTION
        )
```

### Scaledown API Settings

Located in `backend/scaledown.py`:

```python
class ScaledownCompressor:
    def __init__(self):
        self.api_url = SCALEDOWN_API_URL
        self.timeout = SCALEDOWN_TIMEOUT  # 15 seconds
        self.default_rate = SCALEDOWN_RATE  # 'auto'
```

---

## Data Configuration

### College Data Files

Located in `college_data/`:

- **admissions.txt** - Admission requirements, deadlines, documents
- **programs.txt** - Program catalog, courses, placements
- **fees.txt** - Fee structure, scholarships, payment options

#### File Format Requirements

- **Encoding:** UTF-8 (with fallback to Latin-1, CP1252)
- **Format:** Plain text, structured with headers
- **Size:** Total ~60KB recommended for optimal performance

#### Updating Data

```bash
# 1. Edit data files
vim college_data/admissions.txt

# 2. Reload context without restart
curl -X POST http://localhost:5000/reload-context

# Or restart server
python backend/app.py
```

---

### Web Scraping Configuration (Optional)

Located in `backend/config.py`:

```python
SCRAPING_CONFIG = {
    'base_url': 'https://university-website.edu',
    'targets': [
        {
            'url': '/admissions',
            'selectors': {
                'main_content': 'div.content, div.main',
                'requirements': 'ul.requirements',
                'deadlines': 'table.deadlines'
            }
        }
    ],
    'headers': {
        'User-Agent': 'UniversityAdmissionsBot/1.0'
    },
    'timeout': 10  # seconds
}
```

**Enable scraping:**
```bash
SCRAPING_ENABLED=True
```

---

## Performance Tuning

### Cache Strategy

**Global Context Cache** (Memory):
- Loaded once at startup
- Never expires (until reload)
- ~60KB in memory

**Compressed Context Cache** (Memory):
- Created on first request
- Reused for all subsequent requests
- ~40KB in memory

**Configuration:**

```python
# In backend/app.py
_global_context_cache = None       # 60,125 characters
_compressed_context_cache = None   # 9,793 tokens compressed
```

### Timeout Optimization

**Frontend (script.js):**
```javascript
CONFIG.REQUEST_TIMEOUT = 45000  // 45 seconds
```

**Backend (config.py):**
```python
SCALEDOWN_TIMEOUT = 15  // 15 seconds
```

**Recommendation:**
- Frontend timeout > Backend timeout
- Allows for retries and error handling

### Response Size Limits

```python
# Gemini max tokens
GEMINI_MAX_TOKENS = 1024  # ~750-800 words

# Increase for longer responses
GEMINI_MAX_TOKENS = 2048  # ~1500-1600 words
```

**Trade-offs:**
- Higher tokens = Longer responses = Higher cost
- Lower tokens = Faster responses = Lower cost

---

## Security Settings

### API Key Protection

**Secure Storage:**
```bash
# .env file (never commit to Git)
GEMINI_API_KEY=your_key_here
SCALEDOWN_API_KEY=your_key_here
```

**Access Control:**
```python
# In backend/config.py
API_KEYS = {
    'gemini': os.getenv('GEMINI_API_KEY'),
    'scaledown': os.getenv('SCALEDOWN_API_KEY')
}

# Never log or expose these values
```

### CORS Configuration

**Development (permissive):**
```python
CORS(app)  # Allows all origins
```

**Production (restrictive):**
```python
CORS(app, origins=[
    'https://yourdomain.com',
    'https://www.yourdomain.com'
])
```

### Input Validation

**Frontend (script.js):**
```javascript
CONFIG.MAX_MESSAGE_LENGTH = 500  // characters

// Validation in handleSendMessage()
if (message.length > CONFIG.MAX_MESSAGE_LENGTH) {
    showSnackbar('Message too long');
    return;
}
```

**Backend (app.py):**
```python
if not user_message or len(user_message.strip()) == 0:
    return jsonify(error_response("Message cannot be empty")), 400
```

### XSS Protection

**Frontend (script.js):**
```javascript
function formatMessageText(text) {
    // Escape HTML entities
    const escaped = text
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;');
    // ... then format
}
```

---

## Logging Configuration

### Log Levels

```bash
# In .env
LOG_LEVEL=INFO  # DEBUG, INFO, WARNING, ERROR, CRITICAL
```

### Log Format

```python
# In backend/config.py
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
```

**Example log entry:**
```
2026-02-08 22:15:49,930 - chatbot - INFO - Generating response with Gemini...
```

### Log File Location

```bash
# Default
LOG_FILE=logs/chatbot.log

# Custom location
LOG_DIR=custom_logs
LOG_FILE=custom_logs/app.log
```

### Log Rotation (Recommended for Production)

```python
from logging.handlers import RotatingFileHandler

handler = RotatingFileHandler(
    'logs/chatbot.log',
    maxBytes=10*1024*1024,  # 10 MB
    backupCount=5
)
```

---

## Frontend Configuration

### frontend/script.js

```javascript
const CONFIG = {
    API_BASE_URL: 'http://localhost:5000',  // Change for production
    MAX_MESSAGE_LENGTH: 500,
    SHOW_COMPRESSION_STATS: true,  // Show/hide compression info
    TYPING_DELAY: 500,  // ms before showing typing indicator
    REQUEST_TIMEOUT: 45000  // ms (45 seconds)
};
```

### Production Frontend Configuration

```javascript
const CONFIG = {
    API_BASE_URL: 'https://api.yourdomain.com',
    MAX_MESSAGE_LENGTH: 500,
    SHOW_COMPRESSION_STATS: false,  // Hide technical details
    TYPING_DELAY: 300,  // Faster response feel
    REQUEST_TIMEOUT: 30000  // 30 seconds (tighter)
};
```

---

## Environment-Specific Configurations

### Development

```bash
# .env.development
FLASK_ENV=development
FLASK_DEBUG=True
FLASK_PORT=5000
LOG_LEVEL=DEBUG
CORS_ORIGINS=*
```

### Staging

```bash
# .env.staging
FLASK_ENV=production
FLASK_DEBUG=False
FLASK_PORT=8000
LOG_LEVEL=INFO
CORS_ORIGINS=https://staging.yourdomain.com
```

### Production

```bash
# .env.production
FLASK_ENV=production
FLASK_DEBUG=False
FLASK_PORT=80
LOG_LEVEL=WARNING
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
RATE_LIMIT=20 per minute
```

---

## Configuration Validation

Run the system check script:

```bash
python check_system.py
```

**Validates:**
- ✓ Environment variables set
- ✓ API keys present
- ✓ Required directories exist
- ✓ Data files accessible
- ✓ Python version compatible
- ✓ Dependencies installed

---

## Troubleshooting Configuration Issues

### Issue: API Keys Not Found

```bash
# Check .env file exists
ls -la .env

# Verify content
cat .env | grep API_KEY

# Ensure no quotes around values
# CORRECT:   GEMINI_API_KEY=AIza...
# INCORRECT: GEMINI_API_KEY="AIza..."
```

### Issue: Configuration Not Loading

```python
# Debug in Python shell
from dotenv import load_dotenv
load_dotenv()

import os
print(os.getenv('GEMINI_API_KEY'))  # Should print key
```

### Issue: CORS Errors

```python
# Temporarily allow all origins for testing
CORS(app, origins='*')

# Then restrict for production
CORS(app, origins=['https://yourdomain.com'])
```

---

## Best Practices

1. **Never commit .env to Git**
   - Always use .env.example as template
   - Keep secrets in .env (gitignored)

2. **Use different .env files per environment**
   - .env.development
   - .env.staging
   - .env.production

3. **Validate configuration at startup**
   - Check required variables
   - Fail fast with clear error messages

4. **Log configuration (sanitized)**
   - Log environment, debug mode, ports
   - Never log API keys

5. **Document all configuration options**
   - Keep this guide updated
   - Comment configuration files

---

For implementation details, see:
- [Architecture Overview](ARCHITECTURE.md)
- [API Reference](API_REFERENCE.md)
- [Deployment Guide](DEPLOYMENT.md)
