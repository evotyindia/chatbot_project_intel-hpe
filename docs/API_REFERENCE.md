# API Reference

Complete API documentation for the University Admissions Chatbot backend.

## Base URL

```
Development: http://localhost:5000
Production:  https://your-domain.com/api
```

---

## Table of Contents

1. [Authentication](#authentication)
2. [Endpoints](#endpoints)
   - [POST /chat](#post-chat)
   - [GET /health](#get-health)
   - [POST /reload-context](#post-reload-context)
   - [GET /](#get-)
3. [Data Models](#data-models)
4. [Error Handling](#error-handling)
5. [Rate Limiting](#rate-limiting)
6. [Examples](#examples)

---

## Authentication

Currently, the API does not require authentication for development. For production deployment, consider adding:

- API key authentication
- JWT tokens
- OAuth 2.0

**Production Recommendation:**
```python
@app.before_request
def authenticate():
    api_key = request.headers.get('X-API-Key')
    if api_key != os.getenv('API_KEY'):
        return jsonify({'error': 'Unauthorized'}), 401
```

---

## Endpoints

### POST /chat

Main chatbot endpoint that processes user queries and returns AI-generated responses.

#### Request

**Endpoint:** `POST /chat`

**Headers:**
```http
Content-Type: application/json
```

**Body:**
```json
{
  "message": "What programs do you offer?",
  "history": [
    {
      "user": "When was the university established?",
      "assistant": "The NorthCap University was established in 1996."
    }
  ]
}
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `message` | string | Yes | User's query (max 500 characters) |
| `history` | array | No | Conversation history (max 5 exchanges) |

#### Response

**Success (200 OK):**
```json
{
  "response": "The NorthCap University offers multiple programs:\n\n**Undergraduate:**\n- BCA (3 years)\n- B.Tech in CSE, AI & ML, Data Science, ECE, Mechanical (4 years)\n- BBA (3 years)\n- BA in Psychology and Economics (3 years)\n\n**Postgraduate:**\n- MCA (2 years)\n- MBA (2 years)\n\n**Doctoral:**\n- PhD programs in Engineering, Management, Sciences, and Humanities",
  "compression_stats": {
    "original_tokens": 15845,
    "compressed_tokens": 9793,
    "compression_ratio": 1.62,
    "successful": true,
    "latency_ms": 4744,
    "cached": true
  },
  "error": false
}
```

**Error (400 Bad Request):**
```json
{
  "error": true,
  "error_code": "EMPTY_MESSAGE",
  "message": "Message cannot be empty"
}
```

**Error (500 Internal Server Error):**
```json
{
  "error": true,
  "error_code": "GEMINI_ERROR",
  "message": "Failed to generate response. Please try again."
}
```

#### Curl Example

```bash
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What is the BCA fee?",
    "history": []
  }'
```

#### JavaScript Example

```javascript
async function sendMessage(message) {
  const response = await fetch('http://localhost:5000/chat', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      message: message,
      history: []
    })
  });

  const data = await response.json();
  return data;
}
```

---

### GET /health

Health check endpoint to verify server status and configuration.

#### Request

**Endpoint:** `GET /health`

**Headers:** None required

#### Response

**Success (200 OK):**
```json
{
  "status": "healthy",
  "timestamp": "2026-02-08T22:15:30.123Z",
  "context_loaded": true,
  "context_size": 60125,
  "gemini_configured": true,
  "scaledown_configured": true,
  "details": {
    "python_version": "3.11.0",
    "flask_version": "3.0.0",
    "gemini_model": "gemini-2.5-flash",
    "cache_status": "active"
  }
}
```

**Error (500 Internal Server Error):**
```json
{
  "status": "unhealthy",
  "error": "Context not loaded",
  "timestamp": "2026-02-08T22:15:30.123Z"
}
```

#### Curl Example

```bash
curl -X GET http://localhost:5000/health
```

---

### POST /reload-context

Reloads university data from source files without restarting the server.

#### Request

**Endpoint:** `POST /reload-context`

**Headers:** None required

**Body:** None

#### Response

**Success (200 OK):**
```json
{
  "success": true,
  "message": "Context reloaded successfully",
  "context_size_chars": 60125
}
```

**Error (500 Internal Server Error):**
```json
{
  "error": true,
  "error_code": "RELOAD_ERROR",
  "message": "Failed to reload context"
}
```

#### Curl Example

```bash
curl -X POST http://localhost:5000/reload-context
```

#### Use Case

Use this endpoint when you've updated the data files in `college_data/` and want to refresh the chatbot's knowledge without restarting the server.

```bash
# 1. Edit data files
vim college_data/admissions.txt

# 2. Reload context
curl -X POST http://localhost:5000/reload-context

# 3. New data is now available to chatbot
```

---

### GET /

API information and welcome endpoint.

#### Request

**Endpoint:** `GET /`

**Headers:** None required

#### Response

**Success (200 OK):**
```json
{
  "name": "University Admissions Chatbot API",
  "version": "1.0.0",
  "description": "AI-powered chatbot for university admissions queries",
  "endpoints": {
    "chat": "POST /chat",
    "health": "GET /health",
    "reload": "POST /reload-context"
  },
  "documentation": "https://github.com/your-repo/docs",
  "challenge": "Intel & HPE Gen AI for Gen Z 2025"
}
```

#### Curl Example

```bash
curl -X GET http://localhost:5000/
```

---

## Data Models

### Message Object

```typescript
interface Message {
  message: string;      // User query (required)
  history?: Exchange[]; // Conversation history (optional)
}
```

### Exchange Object

```typescript
interface Exchange {
  user: string;       // User's previous message
  assistant: string;  // Assistant's previous response
}
```

### Chat Response

```typescript
interface ChatResponse {
  response: string;              // AI-generated response
  compression_stats: CompressionStats;
  error: boolean;                // Always false on success
}
```

### Compression Stats

```typescript
interface CompressionStats {
  original_tokens: number;     // Token count before compression
  compressed_tokens: number;   // Token count after compression
  compression_ratio: number;   // Compression efficiency ratio
  successful: boolean;         // Compression API success status
  latency_ms: number;          // Compression API latency
  cached: boolean;             // Whether cached compression was used
}
```

### Error Response

```typescript
interface ErrorResponse {
  error: true;
  error_code: string;  // ERROR_CODE constant
  message: string;     // Human-readable error message
}
```

---

## Error Handling

### Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `INVALID_JSON` | 400 | Malformed JSON in request body |
| `EMPTY_MESSAGE` | 400 | Message field is empty or missing |
| `NO_CONTEXT` | 500 | University data not loaded |
| `GEMINI_ERROR` | 500 | Gemini API call failed |
| `INTERNAL_ERROR` | 500 | Unexpected server error |
| `RELOAD_ERROR` | 500 | Failed to reload context |

### Error Response Structure

All errors follow this format:

```json
{
  "error": true,
  "error_code": "ERROR_CODE",
  "message": "Human-readable error description"
}
```

### Client-Side Error Handling

```javascript
async function handleChat(message) {
  try {
    const response = await fetch('/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message })
    });

    const data = await response.json();

    if (data.error) {
      // Handle API error
      console.error(`Error ${data.error_code}: ${data.message}`);
      displayError(data.message);
      return null;
    }

    return data.response;

  } catch (error) {
    // Handle network error
    console.error('Network error:', error);
    displayError('Cannot connect to server');
    return null;
  }
}
```

---

## Rate Limiting

### Current Status

**Development:** No rate limiting

**Production Recommendation:**

Add Flask-Limiter for rate limiting:

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["100 per hour"],
    storage_uri="redis://localhost:6379"
)

@app.route('/chat', methods=['POST'])
@limiter.limit("20 per minute")
def chat():
    ...
```

### Rate Limit Headers

When implemented, responses will include:

```http
X-RateLimit-Limit: 20
X-RateLimit-Remaining: 15
X-RateLimit-Reset: 1707427200
```

### Rate Limit Exceeded Response

```json
{
  "error": true,
  "error_code": "RATE_LIMIT_EXCEEDED",
  "message": "Too many requests. Please try again in 60 seconds.",
  "retry_after": 60
}
```

---

## Examples

### Example 1: Simple Query

**Request:**
```bash
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is the university address?"}'
```

**Response:**
```json
{
  "response": "The NorthCap University is located at:\nSector 23-A, Gurugram, Haryana, India\n\nNearest Metro: HUDA City Centre (Yellow Line)",
  "compression_stats": {
    "original_tokens": 15845,
    "compressed_tokens": 9793,
    "compression_ratio": 1.62,
    "successful": true,
    "latency_ms": 4744,
    "cached": true
  },
  "error": false
}
```

### Example 2: Query with History

**Request:**
```bash
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "How much is it?",
    "history": [
      {
        "user": "What is the BCA program?",
        "assistant": "BCA (Bachelor of Computer Applications) is a 3-year undergraduate program focused on IT and software development."
      }
    ]
  }'
```

**Response:**
```json
{
  "response": "The BCA program fee is:\n\n- Total for 3 years: INR 5,70,000\n- Annual tuition: INR 1,80,000\n- Per semester: INR 90,000\n\nAdditional costs:\n- Registration fee (one-time): INR 25,000\n- Examination fee per semester: INR 4,500",
  "compression_stats": { ... },
  "error": false
}
```

### Example 3: Health Check

**Request:**
```bash
curl http://localhost:5000/health
```

**Response:**
```json
{
  "status": "healthy",
  "context_loaded": true,
  "context_size": 60125,
  "gemini_configured": true,
  "scaledown_configured": true
}
```

### Example 4: Python Client

```python
import requests

class ChatbotClient:
    def __init__(self, base_url="http://localhost:5000"):
        self.base_url = base_url
        self.history = []

    def send_message(self, message):
        """Send a message and get response"""
        response = requests.post(
            f"{self.base_url}/chat",
            json={
                "message": message,
                "history": self.history[-5:]  # Last 5 exchanges
            }
        )

        data = response.json()

        if data.get('error'):
            raise Exception(f"API Error: {data['message']}")

        # Add to history
        self.history.append({
            "user": message,
            "assistant": data['response']
        })

        return data['response']

    def check_health(self):
        """Check API health"""
        response = requests.get(f"{self.base_url}/health")
        return response.json()

# Usage
client = ChatbotClient()
print(client.check_health())
response = client.send_message("What programs do you offer?")
print(response)
```

---

## Webhook Integration (Future)

For real-time integrations (Slack, Discord, WhatsApp):

```python
@app.route('/webhook', methods=['POST'])
def webhook():
    """Handle webhooks from external platforms"""
    data = request.json
    platform = data.get('platform')
    message = data.get('message')

    # Process message
    response = chat_handler(message)

    # Return in platform-specific format
    if platform == 'slack':
        return jsonify({
            "text": response,
            "response_type": "in_channel"
        })
    elif platform == 'discord':
        return jsonify({
            "content": response
        })

    return jsonify({"response": response})
```

---

## API Versioning (Recommended for Production)

```python
# Version 1 (current)
@app.route('/v1/chat', methods=['POST'])
def chat_v1():
    ...

# Version 2 (future)
@app.route('/v2/chat', methods=['POST'])
def chat_v2():
    # Enhanced features
    ...
```

---

## Performance Considerations

### Response Times

| Scenario | Expected Time | Notes |
|----------|---------------|-------|
| First query | 15-20 seconds | Includes compression |
| Cached queries | 2-5 seconds | Cache hit |
| Health check | <100ms | No AI involved |
| Context reload | 1-3 seconds | File I/O only |

### Optimization Tips

1. **Enable caching** - Always enabled by default
2. **Limit history** - Max 5 exchanges recommended
3. **Short messages** - Better performance
4. **Connection pooling** - Use sessions for multiple requests

```python
import requests

session = requests.Session()
session.post(...)  # Faster than individual requests
```

---

## Testing the API

### Using Postman

1. Import collection from `postman_collection.json`
2. Set environment variable: `BASE_URL = http://localhost:5000`
3. Run tests

### Using Python Tests

```python
def test_chat_endpoint():
    response = requests.post(
        'http://localhost:5000/chat',
        json={'message': 'Test query'}
    )
    assert response.status_code == 200
    data = response.json()
    assert 'response' in data
    assert data['error'] == False
```

---

For detailed implementation guides, see:
- [Architecture Overview](ARCHITECTURE.md)
- [Development Guide](DEVELOPMENT.md)
- [Deployment Guide](DEPLOYMENT.md)
