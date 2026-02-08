# 🚀 QUICK START GUIDE

## University Admissions Chatbot - Get Started in 3 Minutes!

---

## ⚡ TL;DR - Three Steps to Run

```bash
# Step 1: Install dependencies
cd backend
pip install -r requirements.txt

# Step 2: Start backend
python app.py

# Step 3: Open frontend/index.html in browser
```

**Done!** Start asking questions about admissions.

---

## 📋 Prerequisites Checklist

Before you start, make sure you have:

- [ ] **Python 3.8+** installed ([Download](https://python.org))
- [ ] **Gemini API Key** ([Get here](https://makersuite.google.com/app/apikey))
- [ ] **Scaledown API Key** ([Get here](https://scaledown.xyz))

---

## 🔧 OPTION 1: Automated Setup (Recommended)

### Windows

```cmd
start.bat
```

This will:
- Check Python installation
- Install dependencies automatically
- Start the backend server
- Show you instructions

### Linux/Mac

```bash
chmod +x start.sh
./start.sh
```

---

## 🔧 OPTION 2: Manual Setup

### Step 1: Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

**This installs:**
- Flask (web server)
- google-generativeai (Gemini AI)
- pdfplumber (PDF extraction)
- beautifulsoup4 (web scraping)
- requests (API calls)

### Step 2: Configure API Keys

**Your `.env` is already configured!**

I noticed you've already added your API keys to `.env.example`. You have two options:

**Option A: Copy to .env (Recommended for Security)**
```bash
# Windows
copy .env.example .env

# Linux/Mac
cp .env.example .env
```

**Option B: Keep as is**
The system will work either way, but `.env` is more secure.

### Step 3: Start Backend Server

```bash
cd backend
python app.py
```

**Expected output:**
```
============================================================
   UNIVERSITY ADMISSIONS CHATBOT - STARTING
============================================================

✅ Configuration validated
✅ Context loaded successfully

============================================================
SERVER READY
============================================================
Listening on http://0.0.0.0:5000
```

### Step 4: Open Frontend

1. Keep the terminal with backend running
2. Open `frontend/index.html` in your browser:
   - Double-click the file, OR
   - Drag it into your browser, OR
   - Right-click → Open With → Browser

---

## 💬 Try These Questions

Once the chatbot loads:

```
"What are the admission requirements?"
"What programs do you offer in computer science?"
"How much is tuition for international students?"
"When is the application deadline?"
"Do you offer scholarships?"
"What are the housing options?"
```

---

## 🎨 Features You'll See

- **Material Design 3 UI** - Beautiful, modern interface
- **Dark Mode** - Click the moon icon (top-right)
- **Quick Actions** - Click chips for instant questions
- **Typing Indicator** - Shows when AI is thinking
- **Compression Stats** - See token reduction (below input)

---

## 🔍 Verify Everything Works

Run the system check:

```bash
python check_system.py
```

**Should show:**
```
STATUS: ALL CHECKS PASSED!
```

---

## 🐛 Troubleshooting

### "Cannot connect to server"

**Problem:** Frontend can't reach backend

**Fix:**
- Make sure backend is running (`python app.py`)
- Check port 5000 is not blocked
- Try `http://localhost:5000/health` in browser

---

### "GEMINI_API_KEY must be set"

**Problem:** API key not found

**Fix:**
- Make sure `.env` exists (copy from `.env.example`)
- Verify keys are on lines without spaces:
  ```
  GEMINI_API_KEY=your_key_here
  SCALEDOWN_API_KEY=your_key_here
  ```

---

### Dependencies not installing

**Problem:** `pip install` fails

**Fix:**
```bash
# Try upgrading pip first
python -m pip install --upgrade pip

# Then install requirements
pip install -r requirements.txt
```

---

## 📁 What You Have

```
university-admissions-bot/
├── backend/              ← Python server files
├── frontend/             ← HTML/CSS/JS chat interface
├── college_data/         ← Sample university data
├── start.bat            ← Windows launcher
├── start.sh             ← Linux/Mac launcher
├── check_system.py      ← System verification
├── README.md            ← Full documentation
└── PROJECT_STATUS.md    ← Detailed status report
```

---

## 🎯 Next Steps

### Customize Your Data

Add your own university information:

1. Place PDF or TXT files in `college_data/` folder
2. Restart backend (Ctrl+C, then `python app.py` again)
3. Files are automatically loaded!

### Enable Web Scraping

Edit `.env`:
```bash
SCRAPING_ENABLED=True
UNIVERSITY_WEBSITE_URL=https://your-university.edu
```

### Change Colors

Edit `frontend/style.css`:
```css
--md-sys-color-primary: #6750A4;  /* Change to your color */
```

---

## 📚 Learn More

- **Full Documentation**: See `README.md`
- **Project Status**: See `PROJECT_STATUS.md`
- **Code Comments**: Read inline documentation in Python files

---

## 🆘 Need Help?

1. Check `README.md` for detailed guides
2. Run `python check_system.py` for diagnostics
3. Review backend logs in `logs/chatbot.log`

---

## ✅ Success Checklist

You know it's working when:

- [ ] Backend shows "SERVER READY"
- [ ] Frontend loads with welcome message
- [ ] You can type and send messages
- [ ] Bot responds to questions
- [ ] Compression stats appear (optional)

---

## 🎉 You're All Set!

**Enjoy your AI-powered university admissions assistant!**

Built with:
- 🤖 Gemini 2.5 Flash (Google AI)
- 🗜️ Scaledown API (Token compression)
- 🎨 Material Design 3 (Beautiful UI)
- 🐍 Flask + Python (Backend)

---

**Questions? Check README.md for comprehensive documentation!**

*Last updated: February 2025*
