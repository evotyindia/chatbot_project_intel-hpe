"""
Utility functions for University Admissions Chatbot
Handles logging and helper functions
"""

import logging
import os
from pathlib import Path
from datetime import datetime
import json
from config import LOG_DIR, LOG_FILE, LOG_LEVEL, LOG_FORMAT

def setup_logger(name='chatbot', log_file=None, level=None):
    """
    Set up logger with file and console handlers

    Args:
        name: Logger name
        log_file: Path to log file (default: from config)
        level: Logging level (default: from config)

    Returns:
        logging.Logger instance
    """
    if log_file is None:
        log_file = LOG_FILE

    if level is None:
        level = getattr(logging, LOG_LEVEL.upper(), logging.INFO)

    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Avoid duplicate handlers
    if logger.handlers:
        return logger

    # Create formatters
    formatter = logging.Formatter(LOG_FORMAT)

    # File handler
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger

def validate_file_path(file_path, extensions=None):
    """
    Validate if file exists and has correct extension

    Args:
        file_path: Path to file
        extensions: List of allowed extensions (e.g., ['.pdf', '.txt'])

    Returns:
        bool: True if valid, False otherwise
    """
    path = Path(file_path)

    if not path.exists():
        return False

    if not path.is_file():
        return False

    if extensions:
        if path.suffix.lower() not in [ext.lower() for ext in extensions]:
            return False

    return True

def sanitize_text(text):
    """
    Sanitize text by removing excessive whitespace and special characters

    Args:
        text: Input text

    Returns:
        str: Sanitized text
    """
    if not text:
        return ""

    # Remove excessive whitespace
    text = ' '.join(text.split())

    # Remove null bytes
    text = text.replace('\x00', '')

    return text.strip()

def format_file_size(size_bytes):
    """
    Format file size in human-readable format

    Args:
        size_bytes: File size in bytes

    Returns:
        str: Formatted size (e.g., "1.5 MB")
    """
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"

def get_cache_key(url_or_name):
    """
    Generate cache key from URL or name

    Args:
        url_or_name: URL or identifier

    Returns:
        str: Cache key
    """
    import hashlib
    return hashlib.md5(url_or_name.encode()).hexdigest()

def load_json_cache(cache_file):
    """
    Load data from JSON cache file

    Args:
        cache_file: Path to cache file

    Returns:
        dict or None: Cached data or None if not found/expired
    """
    try:
        if not Path(cache_file).exists():
            return None

        with open(cache_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Check if cache is expired
        if 'timestamp' in data:
            from config import CACHE_TTL
            cache_time = datetime.fromisoformat(data['timestamp'])
            age = (datetime.now() - cache_time).total_seconds()

            if age > CACHE_TTL:
                return None

        return data

    except Exception as e:
        logger = logging.getLogger('chatbot')
        logger.warning(f"Failed to load cache from {cache_file}: {e}")
        return None

def save_json_cache(cache_file, data):
    """
    Save data to JSON cache file with timestamp

    Args:
        cache_file: Path to cache file
        data: Data to cache

    Returns:
        bool: True if successful
    """
    try:
        # Add timestamp
        cache_data = {
            'timestamp': datetime.now().isoformat(),
            'data': data
        }

        # Ensure cache directory exists
        Path(cache_file).parent.mkdir(parents=True, exist_ok=True)

        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump(cache_data, f, indent=2, ensure_ascii=False)

        return True

    except Exception as e:
        logger = logging.getLogger('chatbot')
        logger.error(f"Failed to save cache to {cache_file}: {e}")
        return False

def truncate_text(text, max_length=1000, suffix='...'):
    """
    Truncate text to maximum length

    Args:
        text: Input text
        max_length: Maximum length
        suffix: Suffix to add when truncated

    Returns:
        str: Truncated text
    """
    if len(text) <= max_length:
        return text

    return text[:max_length - len(suffix)] + suffix

def measure_execution_time(func):
    """
    Decorator to measure function execution time

    Usage:
        @measure_execution_time
        def my_function():
            pass
    """
    import functools
    import time

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger = logging.getLogger('chatbot')
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        logger.debug(f"{func.__name__} executed in {execution_time:.2f} seconds")
        return result

    return wrapper

def format_compression_stats(stats):
    """
    Format compression statistics for logging

    Args:
        stats: Dictionary with compression statistics

    Returns:
        str: Formatted statistics
    """
    if not stats:
        return "No compression stats available"

    original = stats.get('original_tokens', 0)
    compressed = stats.get('compressed_tokens', 0)
    ratio = stats.get('compression_ratio', 1.0)

    if original > 0:
        savings_pct = ((original - compressed) / original) * 100
        return (f"Compression: {original} → {compressed} tokens "
                f"({savings_pct:.1f}% reduction, {ratio:.2f}x compression)")

    return "Compression stats incomplete"

def create_error_response(message, error_code=None):
    """
    Create standardized error response

    Args:
        message: Error message
        error_code: Optional error code

    Returns:
        dict: Error response
    """
    response = {
        'error': True,
        'message': message
    }

    if error_code:
        response['error_code'] = error_code

    return response

def create_success_response(data, message=None):
    """
    Create standardized success response

    Args:
        data: Response data
        message: Optional success message

    Returns:
        dict: Success response
    """
    response = {
        'error': False,
        'data': data
    }

    if message:
        response['message'] = message

    return response

# Initialize default logger
logger = setup_logger()

if __name__ == '__main__':
    # Test logger
    logger.info("Utils module loaded successfully")
    logger.debug("Debug message test")
    logger.warning("Warning message test")
    logger.error("Error message test")

    # Test sanitize
    text = "Test   with   excessive    whitespace\n\nand newlines"
    print(f"Original: {repr(text)}")
    print(f"Sanitized: {repr(sanitize_text(text))}")

    # Test file size formatting
    print(f"1024 bytes = {format_file_size(1024)}")
    print(f"1048576 bytes = {format_file_size(1048576)}")

    # Test compression stats
    stats = {
        'original_tokens': 1000,
        'compressed_tokens': 350,
        'compression_ratio': 2.86
    }
    print(format_compression_stats(stats))
