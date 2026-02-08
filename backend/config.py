"""
Configuration Management for University Admissions Chatbot
Handles environment variables and application settings
"""

import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from .env file
load_dotenv()

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# API Keys
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')
SCALEDOWN_API_KEY = os.getenv('SCALEDOWN_API_KEY', '')

# Flask Configuration
FLASK_ENV = os.getenv('FLASK_ENV', 'development')
FLASK_DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
FLASK_PORT = int(os.getenv('FLASK_PORT', 5000))
FLASK_HOST = os.getenv('FLASK_HOST', '0.0.0.0')

# Web Scraping Configuration
UNIVERSITY_WEBSITE_URL = os.getenv('UNIVERSITY_WEBSITE_URL', 'https://university-website.edu')
SCRAPING_ENABLED = os.getenv('SCRAPING_ENABLED', 'False').lower() == 'true'
CACHE_TTL = int(os.getenv('CACHE_TTL', 3600))  # 1 hour default

# Scraping targets (configurable CSS selectors)
SCRAPING_CONFIG = {
    'base_url': UNIVERSITY_WEBSITE_URL,
    'targets': [
        {
            'url': '/admissions',
            'selectors': {
                'main_content': 'div.content, div.main, article',
                'requirements': 'ul.requirements, .requirements-list',
                'deadlines': 'table.deadlines, .deadline-info'
            }
        },
        {
            'url': '/programs',
            'selectors': {
                'program_list': 'div.program-card, .program-item',
                'description': 'p.description, .program-description'
            }
        },
        {
            'url': '/tuition',
            'selectors': {
                'tuition_table': 'table.tuition, .tuition-info',
                'fees': '.fees-list, table.fees'
            }
        }
    ],
    'headers': {
        'User-Agent': 'UniversityAdmissionsBot/1.0 (Educational Purpose)'
    },
    'timeout': 10  # seconds
}

# Data Paths
COLLEGE_DATA_DIR = BASE_DIR / os.getenv('COLLEGE_DATA_DIR', 'college_data')
CACHE_DIR = BASE_DIR / os.getenv('CACHE_DIR', 'cache')
LOG_DIR = BASE_DIR / os.getenv('LOG_DIR', 'logs')

# Ensure directories exist
CACHE_DIR.mkdir(exist_ok=True)
LOG_DIR.mkdir(exist_ok=True)

# Gemini Model Configuration
GEMINI_MODEL = os.getenv('GEMINI_MODEL', 'gemini-2.5-flash')
GEMINI_TEMPERATURE = float(os.getenv('GEMINI_TEMPERATURE', 0.7))
GEMINI_MAX_TOKENS = int(os.getenv('GEMINI_MAX_TOKENS', 1024))
GEMINI_TOP_P = float(os.getenv('GEMINI_TOP_P', 0.95))

# Scaledown Configuration
SCALEDOWN_API_URL = 'https://api.scaledown.xyz/compress/raw/'
SCALEDOWN_RATE = os.getenv('SCALEDOWN_RATE', 'auto')
SCALEDOWN_MODEL = os.getenv('SCALEDOWN_MODEL', 'gemini-2.5-flash')
SCALEDOWN_TIMEOUT = 15  # seconds (reduced from 30 for faster response)

# System Prompt for Gemini
SYSTEM_INSTRUCTION = """You are an intelligent University Admissions Assistant for The NorthCap University (NCU), designed to help students with admissions and university-related questions.

Role: Help students with university admissions questions about programs, requirements, deadlines, fees, and application processes.

Guidelines:
- Provide accurate, concise, and student-friendly answers
- Use bullet points and structured formatting when helpful
- IMPORTANT: First, try to answer from the provided university context data
- If specific NCU information is not in the context (like dean names, specific faculty details, exact current dates):
  * Use your general knowledge about university systems and typical practices
  * Provide helpful general information while noting "This is general information - please verify with NCU directly"
  * For specific details not in context, suggest contacting: admissions@ncuindia.edu or +91-124-4191000
- Never say "I don't have that information" without trying to help with general knowledge first
- Be encouraging and supportive
- Keep responses brief but comprehensive - avoid overly long responses
- Cite specific details from the context when available (e.g., "According to NCU data...")
- Format responses clearly without unnecessary asterisks or symbols
- Use plain text formatting: bold, lists, and paragraphs naturally without markdown symbols

Context Data: You have access to official NCU data about admissions requirements, academic programs, tuition fees, deadlines, and contact information. Use this data as your primary source, and supplement with general knowledge when needed."""

# Logging Configuration
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_FILE = LOG_DIR / 'chatbot.log'

# Cache Configuration
CACHE_FILE_PREFIX = 'web_cache'
MAX_CACHE_AGE_SECONDS = CACHE_TTL

# CORS Configuration
CORS_ORIGINS = os.getenv('CORS_ORIGINS', '*').split(',')

# Validation
def validate_config():
    """Validate critical configuration settings"""
    errors = []

    if not GEMINI_API_KEY:
        errors.append("GEMINI_API_KEY is not set in environment variables")

    if not SCALEDOWN_API_KEY:
        errors.append("SCALEDOWN_API_KEY is not set in environment variables")

    if not COLLEGE_DATA_DIR.exists():
        errors.append(f"College data directory does not exist: {COLLEGE_DATA_DIR}")

    return errors

def print_config():
    """Print current configuration (for debugging)"""
    print("=" * 60)
    print("CONFIGURATION SUMMARY")
    print("=" * 60)
    print(f"Flask Environment: {FLASK_ENV}")
    print(f"Flask Debug: {FLASK_DEBUG}")
    print(f"Flask Port: {FLASK_PORT}")
    print(f"Gemini Model: {GEMINI_MODEL}")
    print(f"Scaledown Enabled: {bool(SCALEDOWN_API_KEY)}")
    print(f"Web Scraping: {'Enabled' if SCRAPING_ENABLED else 'Disabled'}")
    print(f"College Data Dir: {COLLEGE_DATA_DIR}")
    print(f"Cache Directory: {CACHE_DIR}")
    print(f"Log Directory: {LOG_DIR}")
    print("=" * 60)

if __name__ == '__main__':
    # Validate and print configuration
    errors = validate_config()
    if errors:
        print("Configuration Errors:")
        for error in errors:
            print(f"  - {error}")
    else:
        print("Configuration validated successfully!")

    print_config()
