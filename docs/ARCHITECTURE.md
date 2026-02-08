# System Architecture

## Table of Contents
1. [Overview](#overview)
2. [High-Level Architecture](#high-level-architecture)
3. [Component Details](#component-details)
4. [Data Flow](#data-flow)
5. [Technology Decisions](#technology-decisions)
6. [Performance Optimizations](#performance-optimizations)
7. [Security Architecture](#security-architecture)

---

## Overview

The University Admissions Chatbot follows a **3-tier architecture** with clear separation of concerns:

1. **Presentation Layer** - Frontend (HTML/CSS/JavaScript)
2. **Application Layer** - Backend (Flask + Python)
3. **Data Layer** - File-based storage + External APIs

### Design Principles

- **Simplicity** - Minimal dependencies, vanilla JavaScript
- **Performance** - Aggressive caching, compression optimization
- **Reliability** - Fallback mechanisms, comprehensive error handling
- **Maintainability** - Clean code structure, extensive documentation
- **Security** - Input validation, API key protection, XSS prevention

---

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   USER (Web Browser)                         │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTP/HTTPS
┌────────────────────────┴────────────────────────────────────┐
│                  FRONTEND LAYER                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ HTML5 + CSS3 + Vanilla JavaScript                    │  │
│  │ - Material Design 3 UI                               │  │
│  │ - Real-time message rendering                        │  │
│  │ - Multi-stage loading indicators                     │  │
│  │ - Request timeout handling (45s)                     │  │
│  │ - XSS protection & input sanitization               │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────────────┬────────────────────────────────────┘
                         │ REST API (JSON)
┌────────────────────────┴────────────────────────────────────┐
│                  BACKEND LAYER (Flask)                       │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ API Routes Layer                                      │  │
│  │ - POST /chat - Main chatbot endpoint                │  │
│  │ - GET  /health - Health check                       │  │
│  │ - POST /reload-context - Data refresh               │  │
│  │ - GET  / - API information                          │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ Business Logic Layer                                  │  │
│  │ - Context Management (ingest.py)                     │  │
│  │ - Compression Pipeline (scaledown.py)                │  │
│  │ - AI Response Generation (gemini_client.py)          │  │
│  │ - Caching Strategy (app.py)                          │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ Utility Layer                                         │  │
│  │ - Configuration (config.py)                          │  │
│  │ - Logging (utils.py)                                 │  │
│  │ - Error Handling                                     │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────┬───────────────────┬───────────────────────────┘
             │                   │
    ┌────────┴────────┐    ┌────┴─────────┐
    │ SCALEDOWN API   │    │ GEMINI API   │
    │ Compression     │    │ AI Model     │
    │ (15s timeout)   │    │ (2.5 Flash)  │
    └─────────────────┘    └──────────────┘
             │
┌────────────┴────────────────────────────────────────────────┐
│                  DATA LAYER                                  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ File System Storage                                   │  │
│  │ - college_data/ (TXT files)                          │  │
│  │ - cache/ (Compressed context)                        │  │
│  │ - logs/ (Application logs)                           │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## Component Details

### 1. Frontend Layer

#### Components

**1.1 User Interface (index.html)**
- Material Design 3 components
- Responsive layout (mobile, tablet, desktop)
- Quick action chips for common queries
- Message history display
- Typing indicators with status updates

**1.2 Styling (style.css)**
- Material Design tokens (colors, typography)
- Light/Dark theme support (prepared)
- Responsive breakpoints
- Animation & transitions
- Accessibility features (keyboard navigation)

**1.3 Application Logic (script.js)**
```javascript
Key Functions:
- handleSendMessage() - Main message handler with timeout
- formatMessageText() - Markdown to HTML conversion
- showTypingIndicator() - Multi-stage status display
- addMessage() - Message rendering
- showCompressionStats() - Performance metrics display
```

**Features:**
- Request timeout: 45 seconds (AbortController)
- Progressive status updates: Processing → Compressing → Generating
- Automatic scroll management
- Input validation (500 char limit)
- History management (localStorage ready)

---

### 2. Backend Layer

#### 2.1 Main Application (app.py)

**Global State Management:**
```python
_global_context_cache = None       # University data cache
_compressed_context_cache = None   # Scaledown compressed cache
```

**API Endpoints:**

| Endpoint | Method | Purpose | Response Time |
|----------|--------|---------|---------------|
| `/chat` | POST | Main chatbot interaction | 2-20s |
| `/health` | GET | Server health check | <100ms |
| `/reload-context` | POST | Refresh university data | 1-3s |
| `/` | GET | API information | <50ms |

**Request Flow (/chat):**
1. Validate incoming JSON
2. Load global context (cached)
3. Check compression cache
4. If cached: Reuse (instant)
5. If not cached: Compress via Scaledown (15s)
6. Generate response via Gemini (2-5s)
7. Return response + compression stats

---

#### 2.2 Gemini Client (gemini_client.py)

**Purpose:** Interface with Google Gemini API

```python
class GeminiClient:
    model: GenerativeModel (gemini-2.5-flash)
    temperature: 0.7
    max_tokens: 1024
    top_p: 0.95
```

**Key Methods:**
- `generate_response()` - Main generation with conversation history
- `__build_prompt()` - Construct full prompt with context
- Error handling with retries

**System Instruction:**
- Use context data first
- Fall back to general knowledge if needed
- Never say "I don't know" without helping
- Format responses cleanly (no markdown symbols)

---

#### 2.3 Scaledown Integration (scaledown.py)

**Purpose:** Context compression for token optimization

**Class: ScaledownCompressor**

```python
Compression Pipeline:
1. Receive context (60K chars) + user query
2. HTTP POST to Scaledown API
3. Return compressed prompt + stats
4. Fallback: Return uncompressed if API fails
```

**Configuration:**
- API URL: https://api.scaledown.xyz/compress/raw/
- Timeout: 15 seconds (reduced from 30)
- Compression rate: 'auto'
- Target model: gemini-2.5-flash

**Performance:**
- Original: 15,845 tokens
- Compressed: 9,793 tokens
- Ratio: 1.62x (60% reduction)
- Latency: ~4-5 seconds

---

#### 2.4 Data Ingestion (ingest.py)

**Purpose:** Load and process university data

**Data Sources:**
1. **Local Files** (`college_data/`)
   - admissions.txt (13.6 KB)
   - programs.txt (24.4 KB)
   - fees.txt (21.9 KB)

2. **Web Scraping** (Optional, disabled by default)
   - BeautifulSoup4 for HTML parsing
   - Configurable selectors
   - Cache with TTL (1 hour)

**Processing Pipeline:**
```python
load_local_data()
  ↓
Read TXT files (UTF-8 with fallbacks)
  ↓
Merge into single context string
  ↓
Cache globally (_global_context_cache)
  ↓
Return to application
```

**Features:**
- Encoding detection (UTF-8, Latin-1, CP1252)
- Error handling per file
- Execution time measurement
- Comprehensive logging

---

#### 2.5 Configuration (config.py)

**Environment Variables:**
```bash
GEMINI_API_KEY          # Required
SCALEDOWN_API_KEY       # Required
FLASK_ENV               # development/production
FLASK_DEBUG             # True/False
FLASK_PORT              # Default: 5000
```

**Key Settings:**
- Gemini model: gemini-2.5-flash
- Scaledown timeout: 15s
- Compression rate: auto
- Cache TTL: 3600s

---

## Data Flow

### Request Flow Diagram

```
User Input
    ↓
[Frontend] Validate & Display
    ↓
[Frontend] Show "Processing..." indicator
    ↓
[Frontend] HTTP POST /chat with timeout (45s)
    ↓
[Backend] Receive request
    ↓
[Backend] Load global context (cached)
    ↓
[Backend] Check compression cache
    ├─ Cached? → Reuse compressed context (instant)
    └─ Not cached? → Compress via Scaledown (15s)
    ↓
[Backend] Update indicator: "Generating response..."
    ↓
[Backend] Generate via Gemini (2-5s)
    ↓
[Backend] Return JSON response
    ↓
[Frontend] Display response
    ↓
[Frontend] Show compression stats (5s auto-hide)
    ↓
[Frontend] Update conversation history
```

### Caching Strategy

**Two-Level Cache:**

1. **Global Context Cache** (Memory)
   - Loaded once at startup
   - Updated only on `/reload-context`
   - Stores raw university data (60K chars)

2. **Compressed Context Cache** (Memory)
   - Created on first chat request
   - Reused for all subsequent requests
   - Stores Scaledown compressed prompt
   - Invalidated on context reload

**Performance Impact:**
- First request: ~15-20 seconds (compression + generation)
- Subsequent requests: ~2-5 seconds (generation only)
- 87% improvement in response time

---

## Technology Decisions

### Why Flask?

✅ Lightweight and fast for API development
✅ Minimal setup, easy to understand
✅ Excellent for small to medium projects
✅ Great Python library ecosystem
✅ Simple deployment options

### Why Vanilla JavaScript?

✅ No build process required
✅ Zero dependencies → faster load times
✅ Full control over behavior
✅ Easy to understand and modify
✅ Perfect for project submissions

### Why File-Based Storage?

✅ Simple to set up and maintain
✅ No database overhead
✅ Easy data updates (edit TXT files)
✅ Portable and version-controllable
✅ Sufficient for read-only chatbot

### Why Gemini 2.5 Flash?

✅ Fast inference (~2-5s)
✅ Cost-effective for high volume
✅ Excellent instruction following
✅ Good context understanding
✅ Free tier available for development

### Why Scaledown API?

✅ 60% token reduction
✅ Cost savings on Gemini API
✅ Faster inference (fewer tokens)
✅ No quality degradation
✅ Simple REST API integration

---

## Performance Optimizations

### 1. Context Compression

**Problem:** 60K character context = expensive API calls

**Solution:** Scaledown compression
- Reduces 15,845 → 9,793 tokens (38% reduction)
- Saves $0.03 per request (at scale)
- Faster Gemini inference

### 2. Smart Caching

**Problem:** Re-compression on every request

**Solution:** Memory-based cache
- First request: Compress and cache
- Subsequent requests: Reuse cache
- 87% faster response time

### 3. Timeout Optimization

**Problem:** Long wait times with no feedback

**Solution:**
- Reduced Scaledown timeout: 30s → 15s
- Frontend timeout: 45s with AbortController
- Multi-stage loading indicators

### 4. Lazy Loading

**Context loaded once at startup:**
- Avoid repeated file reads
- Faster request handling
- Consistent data across requests

### 5. Minimal Dependencies

**Frontend:** Zero npm dependencies
- Faster page load
- No build process
- Reduced complexity

---

## Security Architecture

### 1. API Key Protection

**Storage:**
```
.env (gitignored)       ← API keys stored here
.env.example (tracked)  ← Template without secrets
```

**Access:**
- Environment variables only
- Never hardcoded
- Never logged
- Never sent to frontend

### 2. Input Validation

**Frontend:**
- Max message length: 500 characters
- Character escaping for XSS protection
- Input sanitization before display

**Backend:**
- JSON validation
- Empty message rejection
- Type checking

### 3. CORS Configuration

```python
CORS(app)  # Currently: Allow all (development)
```

**Production:** Restrict to specific origins
```python
CORS(app, origins=['https://your-domain.com'])
```

### 4. Error Handling

**Never expose:**
- Stack traces to users
- Internal error details
- API keys in error messages
- File paths

**Do expose:**
- User-friendly error messages
- Retry suggestions
- Contact information

### 5. Rate Limiting (Recommended for Production)

```python
# Add Flask-Limiter
from flask_limiter import Limiter

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["100 per hour"]
)

@app.route('/chat')
@limiter.limit("20 per minute")
def chat():
    ...
```

---

## Scalability Considerations

### Current Limitations

- Single-threaded Flask development server
- In-memory caching (lost on restart)
- No database for persistence
- No load balancing

### Future Improvements

**1. Production Server**
```bash
# Replace development server with
gunicorn -w 4 -b 0.0.0.0:5000 backend.app:app
```

**2. Persistent Cache**
```python
# Add Redis for caching
import redis
cache = redis.Redis(host='localhost', port=6379)
```

**3. Database Integration**
```python
# Add PostgreSQL for conversation history
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)
```

**4. Async Processing**
```python
# Use Celery for background tasks
from celery import Celery
celery = Celery(app.name)
```

---

## Monitoring & Logging

### Current Implementation

**Logging Levels:**
- INFO: Normal operations
- WARNING: Recoverable issues
- ERROR: Failures requiring attention

**Log Files:**
- Location: `logs/chatbot.log`
- Rotation: Manual (add logrotate for production)
- Format: Timestamp, Level, Message

**Key Metrics Logged:**
- Request processing time
- Compression statistics
- API call latency
- Error occurrences

### Production Monitoring (Recommended)

1. **Application Monitoring**
   - Add Sentry for error tracking
   - Prometheus for metrics
   - Grafana for dashboards

2. **Infrastructure Monitoring**
   - CPU/Memory usage
   - Disk space
   - Network latency

3. **Business Metrics**
   - Requests per minute
   - Average response time
   - Error rate
   - User satisfaction

---

## Diagram: Complete Request Flow

```
┌─────────────┐
│   User      │
│   Types     │
│   Message   │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────┐
│ Frontend Validation             │
│ - Length check (500 chars)      │
│ - Sanitize input                │
└──────┬──────────────────────────┘
       │
       ▼
┌─────────────────────────────────┐
│ Display "Processing..."          │
│ Start timeout timer (45s)       │
└──────┬──────────────────────────┘
       │
       ▼
┌─────────────────────────────────┐
│ HTTP POST /chat                 │
│ {message, history}              │
└──────┬──────────────────────────┘
       │
       ▼
┌─────────────────────────────────┐
│ Backend: Validate JSON          │
└──────┬──────────────────────────┘
       │
       ▼
┌─────────────────────────────────┐
│ Load Global Context (cached)    │
│ 60,125 characters               │
└──────┬──────────────────────────┘
       │
       ▼
       ┌───────────┐
       │ Cached?   │
       └─────┬─────┘
         Yes │ No
      ┌──────┴──────┐
      │             │
      ▼             ▼
┌──────────┐  ┌─────────────────┐
│ Reuse    │  │ Compress via    │
│ Cache    │  │ Scaledown       │
│ (instant)│  │ (15s timeout)   │
└────┬─────┘  └────────┬────────┘
     │                 │
     │                 ▼
     │         ┌──────────────┐
     │         │ Cache Result │
     │         └──────┬───────┘
     │                │
     └────────┬───────┘
              ▼
┌─────────────────────────────────┐
│ Update: "Generating response..." │
└──────┬──────────────────────────┘
       │
       ▼
┌─────────────────────────────────┐
│ Gemini API Call                 │
│ - System instruction            │
│ - Compressed context            │
│ - Conversation history          │
│ - User query                    │
└──────┬──────────────────────────┘
       │
       ▼
┌─────────────────────────────────┐
│ Response Generated (2-5s)       │
└──────┬──────────────────────────┘
       │
       ▼
┌─────────────────────────────────┐
│ Return JSON                     │
│ {response, compression_stats}   │
└──────┬──────────────────────────┘
       │
       ▼
┌─────────────────────────────────┐
│ Frontend: Display Response      │
│ - Format markdown               │
│ - Show compression stats        │
│ - Update history                │
└──────┬──────────────────────────┘
       │
       ▼
┌─────────────┐
│ User Reads  │
│ Response    │
└─────────────┘
```

---

**Next Steps:**
- Review [API Reference](API_REFERENCE.md) for endpoint details
- See [Configuration Guide](CONFIGURATION.md) for environment setup
- Check [Development Guide](DEVELOPMENT.md) for contributing
