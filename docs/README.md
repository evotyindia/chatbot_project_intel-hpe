# University Admissions Chatbot - Documentation

![Project Status](https://img.shields.io/badge/Status-Active-success)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Flask](https://img.shields.io/badge/Flask-3.0-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 📚 Documentation Index

This folder contains comprehensive documentation for the AI-Powered University Admissions Chatbot project, developed for the **Intel & HPE Gen AI for Gen Z Challenge 2025**.

### Quick Links

1. **[Architecture Overview](ARCHITECTURE.md)** - System design and components
2. **[Installation Guide](INSTALLATION.md)** - Step-by-step setup instructions
3. **[API Reference](API_REFERENCE.md)** - Complete API documentation
4. **[Configuration Guide](CONFIGURATION.md)** - Environment and system configuration
5. **[Development Guide](DEVELOPMENT.md)** - Contributing and development workflow
6. **[Deployment Guide](DEPLOYMENT.md)** - Production deployment instructions
7. **[Troubleshooting](TROUBLESHOOTING.md)** - Common issues and solutions

---

## 📖 Project Overview

### What is this project?

An intelligent chatbot powered by Google Gemini AI that helps prospective students find instant, accurate information about university admissions, programs, fees, deadlines, and application processes.

### Key Features

✅ **Hybrid Intelligence System**
- Primary: Structured university data (60K+ characters)
- Fallback: Gemini AI general knowledge
- Never says "I don't know" - always provides helpful guidance

✅ **Advanced Performance**
- 87% faster responses with smart caching (30s → 2-5s)
- 60% token compression via Scaledown API
- Real-time processing status updates

✅ **Superior UX**
- Material Design 3 interface
- Multi-stage loading indicators
- Mobile-responsive design
- Quick action chips for common queries

### Technology Stack

**Backend:**
- Python 3.8+
- Flask 3.0
- Google Gemini 2.5 Flash API
- Scaledown Compression API

**Frontend:**
- Vanilla JavaScript (ES6+)
- HTML5 / CSS3
- Material Design 3
- No framework dependencies

**Data Processing:**
- PDFPlumber / PyPDF2 for PDF extraction
- BeautifulSoup4 for web scraping
- Custom context compression pipeline

---

## 🚀 Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/evotyindia/chatbot_project_intel-hpe
cd chatbot_project_intel-hpe

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env
# Edit .env with your API keys

# 4. Start the backend
python backend/app.py

# 5. Open frontend
# Navigate to frontend/index.html in your browser
```

For detailed instructions, see [Installation Guide](INSTALLATION.md).

---

## 📊 Project Structure

```
UAC/
├── backend/              # Flask backend application
│   ├── app.py           # Main Flask server
│   ├── gemini_client.py # Gemini API integration
│   ├── scaledown.py     # Scaledown compression
│   ├── ingest.py        # Data loading & processing
│   ├── config.py        # Configuration management
│   └── utils.py         # Utility functions
├── frontend/            # Frontend application
│   ├── index.html       # Main HTML file
│   ├── style.css        # Material Design styles
│   └── script.js        # Chat logic & API calls
├── college_data/        # University data files
│   ├── admissions.txt   # Admission information
│   ├── programs.txt     # Program catalog
│   └── fees.txt         # Fee structure
├── docs/                # Project documentation
├── cache/               # Cache directory (auto-generated)
├── logs/                # Log files (auto-generated)
├── .env.example         # Environment template
└── requirements.txt     # Python dependencies
```

---

## 🎯 Use Cases

1. **Prospective Students**
   - Find program information instantly
   - Check admission requirements
   - Get fee details and scholarships
   - Learn about application deadlines

2. **Academic Institutions**
   - Automate admission query responses
   - Reduce staff workload
   - Provide 24/7 student support
   - Scale information access

3. **Educational Technology**
   - Demonstrate Gen AI applications
   - Show context-aware chatbot design
   - Illustrate hybrid intelligence systems

---

## 📈 Performance Metrics

| Metric | Value | Impact |
|--------|-------|--------|
| Response Time (Cached) | 2-5 seconds | 87% faster than initial |
| Response Time (First) | 15-20 seconds | Due to compression overhead |
| Token Compression | 60% reduction | 15,845 → 9,793 tokens |
| Context Size | 60,125 characters | Comprehensive data coverage |
| Cache Hit Rate | ~95% | After first query |
| Compression Ratio | 1.62x | Scaledown API efficiency |

---

## 🔒 Security Considerations

- **API Keys**: Stored in `.env` (never committed to Git)
- **Input Validation**: All user inputs sanitized
- **XSS Protection**: HTML escaping on frontend
- **CORS**: Properly configured for localhost
- **Rate Limiting**: Consider adding for production
- **HTTPS**: Required for production deployment

---

## 🤝 Contributing

We welcome contributions! Please see:
- [Development Guide](DEVELOPMENT.md) for coding standards
- [Architecture Overview](ARCHITECTURE.md) for system design
- Create issues for bugs or feature requests

---

## 📄 License

This project is licensed under the MIT License. See LICENSE file for details.

---

## 🙏 Acknowledgments

- **Intel & HPE** - Gen AI for Gen Z Challenge organizers
- **The NorthCap University** - Sample data and opportunity
- **Google Gemini Team** - AI model and API
- **Scaledown.xyz** - Context compression service
- Faculty mentors and team members

---

## 📞 Support

For questions or issues:
- Create a GitHub Issue
- Contact project maintainers
- Refer to [Troubleshooting Guide](TROUBLESHOOTING.md)

---

## 🗺️ Roadmap

### Completed ✅
- Core chatbot functionality
- Gemini AI integration
- Context compression
- Material Design UI
- Smart caching system
- Multi-stage loading indicators

### Planned 🔜
- Multi-language support
- Voice input/output
- Mobile app (React Native)
- Analytics dashboard
- Advanced RAG implementation
- Database integration
- User authentication
- Admin panel

---

**Built with ❤️ for the Intel & HPE Gen AI for Gen Z Challenge 2025**
