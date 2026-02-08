# 🎓 University Admissions Bot

A **modern, production-ready AI chatbot** that helps students navigate university admissions using **local documents (PDF/TXT)** and **live online data**, powered by **Gemini 2.5 Flash** with **token compression (Scaledown)**.

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Flask](https://img.shields.io/badge/Flask-3.0-green)
![Material Design 3](https://img.shields.io/badge/Material%20Design-3-purple)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Architecture](#architecture)
- [Customization](#customization)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## 🚀 Overview

The University Admissions Bot is an intelligent chatbot that helps prospective students get accurate information about:

- **Admission Requirements**: GPA, test scores, deadlines, documents
- **Academic Programs**: Available majors, courses, specializations
- **Tuition & Fees**: Costs, financial aid, scholarships, payment plans
- **Application Process**: Step-by-step guidance for applying
- **International Students**: TOEFL/IELTS requirements, visa information

### How It Works

1. **Data Ingestion**: Extracts text from local PDF/TXT files in `college_data/`
2. **Web Scraping** (Optional): Fetches live data from university website
3. **Data Merging**: Combines local + online data into unified context
4. **Scaledown Compression**: Compresses context using Scaledown API (reduces tokens by 50-70%)
5. **Gemini AI**: Generates accurate responses using Gemini 2.5 Flash
6. **Material Design UI**: Clean, modern chat interface

---

## ✨ Features

### Core Features

- ✅ **PDF & TXT Extraction**: Automatically reads university data files
- ✅ **Live Web Scraping**: Optional fetching of real-time university data
- ✅ **Scaledown Compression**: Mandatory 50-70% token reduction before AI processing
- ✅ **Gemini 2.5 Flash AI**: Fast, accurate responses
- ✅ **Conversation History**: Maintains context across multiple questions
- ✅ **Material Design 3**: Beautiful, accessible UI with dark mode

### User Experience

- 🎨 Material Design 3 interface (light & dark themes)
- 💬 Real-time chat with typing indicators
- 📊 Compression statistics display (optional)
- ⚡ Quick action chips for common questions
- 📱 Fully responsive (mobile, tablet, desktop)
- ⌨️ Keyboard shortcuts (Ctrl+K to focus, Ctrl+L to clear)

### Technical Features

- 🔒 Secure API key management via environment variables
- 📝 Comprehensive logging (DEBUG, INFO, WARNING, ERROR levels)
- 💾 Intelligent caching for web-scraped data
- 🛡️ Error handling with graceful degradation
- 🔄 Auto-reload context without server restart
- 🧪 Built-in health check endpoint

---

## 🛠️ Tech Stack

### Backend
- **Python 3.8+**
- **Flask 3.0**: Web framework
- **Gemini 2.5 Flash**: Google's AI model
- **Scaledown API**: Token compression service
- **pdfplumber/PyPDF2**: PDF text extraction
- **BeautifulSoup4**: Web scraping

### Frontend
- **HTML5**: Semantic markup
- **CSS3**: Material Design 3 styling
- **Vanilla JavaScript**: No framework dependencies
- **Material Icons**: Google's icon font

---

## 📁 Project Structure

```
university-admissions-bot/
│
├── backend/
│   ├── app.py                # Flask server & API endpoints
│   ├── config.py             # Configuration management
│   ├── utils.py              # Logging and helper functions
│   ├── ingest.py             # PDF/TXT extraction & web scraping
│   ├── scaledown.py          # Scaledown compression integration
│   ├── gemini_client.py      # Gemini AI integration
│   └── requirements.txt      # Python dependencies
│
├── frontend/
│   ├── index.html            # Chat UI structure
│   ├── style.css             # Material Design 3 styles
│   └── script.js             # Frontend logic
│
├── college_data/             # University data files
│   ├── admissions.txt        # Admissions info
│   ├── programs.txt          # Academic programs
│   └── fees.txt              # Tuition & fees
│
├── cache/                    # Cached web data (auto-created)
├── logs/                     # Application logs (auto-created)
│
├── .env                      # API keys (create from .env.example)
├── .env.example              # Environment template
├── .gitignore                # Git ignore rules
└── README.md                 # This file
```

---

## 📦 Prerequisites

Before you begin, ensure you have:

- **Python 3.8 or higher** ([Download](https://www.python.org/downloads/))
- **pip** (Python package manager, included with Python)
- **Gemini API Key** ([Get it here](https://makersuite.google.com/app/apikey))
- **Scaledown API Key** ([Get it here](https://scaledown.xyz))
- **Internet connection** (for API calls and optional web scraping)

---

## 🔧 Installation

### 1. Clone or Download the Project

```bash

git clone https://github.com/evotyindia/chatbot_project_intel-hpe
cd chatbot_project_intel-hpe

```

### 2. Create Virtual Environment (Recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

This will install the following packages:
- Flask==3.0.0
- flask-cors==4.0.0
- python-dotenv==1.0.0
- google-generativeai==0.3.0
- requests==2.31.0
- PyPDF2==3.0.1
- pdfplumber==0.10.3
- beautifulsoup4==4.12.0
- lxml==4.9.3

---

## ⚙️ Configuration

### 1. Create Environment File

```bash
# Copy the example file
cp .env.example .env

# Or on Windows:
copy .env.example .env
```

### 2. Add Your API Keys

Open `.env` in a text editor and add your keys:

```bash
# Required API Keys
GEMINI_API_KEY=your_actual_gemini_api_key_here
SCALEDOWN_API_KEY=your_actual_scaledown_api_key_here
```

### 3. Configure Optional Settings

Adjust these settings in `.env` as needed:

```bash
# Enable/disable web scraping
SCRAPING_ENABLED=False

# University website to scrape (if enabled)
UNIVERSITY_WEBSITE_URL=https://your-university.edu

# Flask server port
FLASK_PORT=5000

# Logging level
LOG_LEVEL=INFO
```

See `.env.example` for all available configuration options.

---

## 🚀 Running the Application

### 1. Start the Backend Server

```bash
# Navigate to backend directory
cd backend

# Run the Flask app
python app.py
```

You should see:

```
============================================================
UNIVERSITY ADMISSIONS CHATBOT - STARTING
============================================================

✅ Configuration validated

============================================================
CONFIGURATION SUMMARY
============================================================
Flask Environment: development
Flask Debug: True
Flask Port: 5000
...

============================================================
SERVER READY
============================================================
Listening on http://0.0.0.0:5000
Press CTRL+C to stop
============================================================
```

### 2. Open the Frontend

Open `frontend/index.html` in your web browser:

```bash
# Navigate to frontend directory
cd ../frontend

# Open in default browser (Windows)
start index.html

# Or (macOS)
open index.html

# Or (Linux)
xdg-open index.html
```

**Or simply drag `frontend/index.html` into your browser.**

### 3. Start Chatting!

Type questions like:
- "What are the admission requirements?"
- "What programs do you offer in engineering?"
- "How much is tuition for international students?"
- "When is the application deadline?"

---

## 💬 Usage

### Basic Chat

1. Type your question in the input field
2. Press **Enter** or click the **Send button**
3. Wait for the AI response (typing indicator shows progress)
4. Continue the conversation naturally

### Quick Actions

Click the **quick action chips** below the input for instant questions:
- Requirements
- Programs
- Tuition
- Deadlines

### Keyboard Shortcuts

- **Enter**: Send message
- **Ctrl/Cmd + K**: Focus input field
- **Ctrl/Cmd + L**: Clear chat history (after confirmation)
- **Escape**: Blur input field

### Dark Mode

Click the **moon/sun icon** in the top-right to toggle between light and dark themes.

### Compression Stats

If enabled in `frontend/script.js` (set `SHOW_COMPRESSION_STATS: true`), you'll see compression statistics below the input after each response, showing token reduction percentage.

---

## 📡 API Documentation

### Base URL

```
http://localhost:5000
```

### Endpoints

#### `GET /`
**Description**: API information

**Response**:
```json
{
  "service": "University Admissions Chatbot API",
  "version": "1.0.0",
  "endpoints": {...}
}
```

---

#### `GET /health`
**Description**: Health check

**Response**:
```json
{
  "status": "healthy",
  "context_loaded": true,
  "context_size_chars": 45123,
  "components": {
    "data_ingestion": true,
    "scaledown": true,
    "gemini": true
  }
}
```

---

#### `POST /chat`
**Description**: Main chatbot endpoint

**Request Body**:
```json
{
  "message": "What is the application deadline?",
  "history": [
    {
      "user": "Previous question",
      "assistant": "Previous answer"
    }
  ]
}
```

**Response**:
```json
{
  "response": "The application deadline is January 15, 2025...",
  "compression_stats": {
    "original_tokens": 1000,
    "compressed_tokens": 350,
    "compression_ratio": 2.86,
    "successful": true,
    "latency_ms": 2341
  },
  "error": false
}
```

---

#### `POST /reload-context`
**Description**: Reload university data without restarting server

**Response**:
```json
{
  "success": true,
  "message": "Context reloaded successfully",
  "context_size_chars": 45000
}
```

---

## 🏗️ Architecture

### Data Flow

```
┌─────────────────┐
│  College Data   │ (PDF/TXT files)
│  + Web Scraping │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Data Ingestion │ (ingest.py)
│  & Merging      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Scaledown     │ (scaledown.py)
│  Compression    │ ← MANDATORY: Reduces tokens by 50-70%
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Gemini 2.5 Flash│ (gemini_client.py)
│   AI Response   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Flask API     │ (app.py)
│   /chat endpoint│
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Frontend UI    │ (Material Design 3)
│   Chat Interface│
└─────────────────┘
```

### Key Design Principles

1. **Compression-First**: ALL data to Gemini MUST pass through Scaledown
2. **Modular Architecture**: Separate concerns (ingestion, compression, AI, presentation)
3. **Error Resilience**: Graceful degradation at every layer
4. **Caching Strategy**: Cache web data and compressed prompts
5. **Logging**: Comprehensive logging for debugging

---

## 🎨 Customization

### Add More University Data

1. Place PDF or TXT files in `college_data/` directory
2. Files are automatically loaded on server start
3. No code changes needed!

### Change AI Behavior

Edit the system instruction in `backend/config.py`:

```python
SYSTEM_INSTRUCTION = """
Your custom instructions here...
"""
```

### Modify UI Colors

Edit Material Design 3 color tokens in `frontend/style.css`:

```css
:root {
    --md-sys-color-primary: #6750A4;  /* Change this */
    --md-sys-color-on-primary: #FFFFFF;
    ...
}
```

### Enable Web Scraping

1. Set `SCRAPING_ENABLED=True` in `.env`
2. Configure `UNIVERSITY_WEBSITE_URL`
3. Adjust CSS selectors in `backend/config.py` → `SCRAPING_CONFIG`

---

## 🐛 Troubleshooting

### Backend Won't Start

**Problem**: `GEMINI_API_KEY must be set`

**Solution**:
- Check that `.env` file exists
- Verify API keys are correctly set
- Make sure you're in the `backend/` directory when running `python app.py`

---

### "Cannot connect to server" Error

**Problem**: Frontend can't reach backend

**Solution**:
- Make sure backend is running (`python app.py` in backend directory)
- Check that Flask is listening on port 5000
- Try changing `API_BASE_URL` in `frontend/script.js` to `http://127.0.0.1:5000`

---

### PDF Extraction Fails

**Problem**: Error reading PDF files

**Solution**:
- Ensure `pdfplumber` is installed: `pip install pdfplumber`
- Check that PDF files are not corrupted
- Try converting PDFs to TXT files if extraction continues to fail

---

### Compression Not Working

**Problem**: Scaledown API errors

**Solution**:
- Verify `SCALEDOWN_API_KEY` is correct
- Check internet connection
- The system will fall back to uncompressed prompts if Scaledown fails (warning logged)

---

### High Token Usage

**Problem**: Scaledown not compressing enough

**Solution**:
- Check that `SCALEDOWN_API_KEY` is set (compression is mandatory)
- Verify compression stats in logs
- Consider reducing context size in `college_data/` files

---

## 🤝 Contributing

Contributions are welcome! Here's how:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Make your changes
4. Test thoroughly
5. Commit (`git commit -m 'Add some feature'`)
6. Push (`git push origin feature/your-feature`)
7. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License.

---

## 📞 Support

For issues or questions:

- **Create an issue** on GitHub
- **Email**: support@university-chatbot.dev (example)
- **Documentation**: See this README and code comments

---

## 🙏 Acknowledgments

- **Google Gemini**: For the powerful AI model
- **Scaledown**: For efficient token compression
- **Material Design**: For the beautiful design system
- **Flask**: For the lightweight web framework

---

## 📊 System Requirements

- **Python**: 3.8 or higher
- **RAM**: 2GB minimum, 4GB recommended
- **Disk Space**: 500MB for dependencies and data
- **Internet**: Required for API calls

---

## 🔮 Future Enhancements

Potential improvements:

- [ ] Multi-language support (Spanish, Chinese, etc.)
- [ ] Voice input/output
- [ ] More interactive visualizations (charts for tuition, etc.)
- [ ] Comparison tool for multiple programs
- [ ] Email integration for sending transcripts
- [ ] Calendar integration for deadline reminders
- [ ] Admin panel for managing data files
- [ ] Analytics dashboard for popular questions

---

## 📚 Additional Resources

- [Gemini API Documentation](https://ai.google.dev/docs)
- [Scaledown API Documentation](https://scaledown.xyz/docs)
- [Material Design 3](https://m3.material.io/)
- [Flask Documentation](https://flask.palletsprojects.com/)

---

**Built with ❤️ for students navigating university admissions**

*Last Updated: February 2025*
