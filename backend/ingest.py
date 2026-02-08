"""
Data Ingestion Module for University Admissions Chatbot
Handles PDF/TXT extraction, web scraping, and data merging
"""

import os
from pathlib import Path
from typing import Dict, List, Optional
import requests
from bs4 import BeautifulSoup
from utils import logger, sanitize_text, validate_file_path, get_cache_key, load_json_cache, save_json_cache, measure_execution_time
from config import COLLEGE_DATA_DIR, CACHE_DIR, SCRAPING_CONFIG, SCRAPING_ENABLED

# Try importing PDF libraries with fallbacks
try:
    import pdfplumber
    PDF_LIBRARY = 'pdfplumber'
except ImportError:
    try:
        import PyPDF2
        PDF_LIBRARY = 'PyPDF2'
    except ImportError:
        PDF_LIBRARY = None
        logger.warning("No PDF library available. PDF extraction will fail.")


def extract_text_from_pdf(file_path: str) -> Dict[str, any]:
    """
    Extract text from PDF file

    Args:
        file_path: Path to PDF file

    Returns:
        dict: {filename, content, metadata, error}
    """
    result = {
        'filename': Path(file_path).name,
        'content': '',
        'metadata': {},
        'error': None
    }

    try:
        if not validate_file_path(file_path, ['.pdf']):
            result['error'] = "Invalid PDF file path"
            return result

        if PDF_LIBRARY == 'pdfplumber':
            # Use pdfplumber (better for tables and structure)
            with pdfplumber.open(file_path) as pdf:
                result['metadata']['pages'] = len(pdf.pages)
                text_parts = []

                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text_parts.append(page_text)

                result['content'] = '\n\n'.join(text_parts)

        elif PDF_LIBRARY == 'PyPDF2':
            # Fallback to PyPDF2
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                result['metadata']['pages'] = len(pdf_reader.pages)
                text_parts = []

                for page in pdf_reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text_parts.append(page_text)

                result['content'] = '\n\n'.join(text_parts)

        else:
            result['error'] = "No PDF library available"
            return result

        # Sanitize extracted text
        result['content'] = sanitize_text(result['content'])
        logger.info(f"Extracted {len(result['content'])} characters from {result['filename']}")

    except Exception as e:
        logger.error(f"Error extracting PDF {file_path}: {e}")
        result['error'] = str(e)

    return result


def extract_text_from_txt(file_path: str) -> Dict[str, any]:
    """
    Extract text from TXT file

    Args:
        file_path: Path to TXT file

    Returns:
        dict: {filename, content, metadata, error}
    """
    result = {
        'filename': Path(file_path).name,
        'content': '',
        'metadata': {},
        'error': None
    }

    try:
        if not validate_file_path(file_path, ['.txt']):
            result['error'] = "Invalid TXT file path"
            return result

        # Try multiple encodings
        encodings = ['utf-8', 'latin-1', 'cp1252']

        for encoding in encodings:
            try:
                with open(file_path, 'r', encoding=encoding) as file:
                    content = file.read()
                    result['content'] = sanitize_text(content)
                    result['metadata']['encoding'] = encoding
                    logger.info(f"Read {len(result['content'])} characters from {result['filename']} using {encoding}")
                    break
            except UnicodeDecodeError:
                continue

        if not result['content']:
            result['error'] = "Failed to decode text file"

    except Exception as e:
        logger.error(f"Error reading TXT {file_path}: {e}")
        result['error'] = str(e)

    return result


@measure_execution_time
def load_local_data(data_dir: Path = None) -> Dict[str, any]:
    """
    Load all PDF and TXT files from college_data directory

    Args:
        data_dir: Directory containing data files (default: from config)

    Returns:
        dict: {files_data, errors, summary}
    """
    if data_dir is None:
        data_dir = COLLEGE_DATA_DIR

    result = {
        'files_data': {},
        'errors': [],
        'summary': {
            'total_files': 0,
            'successful': 0,
            'failed': 0
        }
    }

    try:
        if not data_dir.exists():
            logger.error(f"Data directory does not exist: {data_dir}")
            result['errors'].append(f"Directory not found: {data_dir}")
            return result

        # Scan for PDF and TXT files
        file_patterns = ['*.pdf', '*.txt']
        all_files = []

        for pattern in file_patterns:
            all_files.extend(data_dir.glob(pattern))

        result['summary']['total_files'] = len(all_files)

        for file_path in all_files:
            file_key = file_path.stem  # filename without extension

            if file_path.suffix.lower() == '.pdf':
                file_data = extract_text_from_pdf(str(file_path))
            elif file_path.suffix.lower() == '.txt':
                file_data = extract_text_from_txt(str(file_path))
            else:
                continue

            if file_data['error']:
                result['errors'].append(f"{file_path.name}: {file_data['error']}")
                result['summary']['failed'] += 1
            else:
                result['files_data'][file_key] = file_data
                result['summary']['successful'] += 1

        logger.info(f"Loaded {result['summary']['successful']} files successfully, "
                   f"{result['summary']['failed']} failed")

    except Exception as e:
        logger.error(f"Error loading local data: {e}")
        result['errors'].append(str(e))

    return result


@measure_execution_time
def scrape_website(config: Dict = None, use_cache: bool = True) -> Dict[str, any]:
    """
    Scrape university website for online data

    Args:
        config: Scraping configuration (default: from config)
        use_cache: Whether to use cached data if available

    Returns:
        dict: {scraped_data, errors, cached}
    """
    if config is None:
        config = SCRAPING_CONFIG

    if not SCRAPING_ENABLED:
        logger.info("Web scraping is disabled in configuration")
        return {'scraped_data': {}, 'errors': [], 'cached': False}

    result = {
        'scraped_data': {},
        'errors': [],
        'cached': False
    }

    try:
        base_url = config['base_url']
        headers = config.get('headers', {})
        timeout = config.get('timeout', 10)

        for target in config['targets']:
            url = base_url + target['url']
            cache_key = get_cache_key(url)
            cache_file = CACHE_DIR / f"web_cache_{cache_key}.json"

            # Try loading from cache first
            if use_cache:
                cached_data = load_json_cache(cache_file)
                if cached_data:
                    result['scraped_data'][target['url']] = cached_data['data']
                    result['cached'] = True
                    logger.info(f"Loaded cached data for {url}")
                    continue

            # Scrape live data
            try:
                response = requests.get(url, headers=headers, timeout=timeout)
                response.raise_for_status()

                soup = BeautifulSoup(response.text, 'html.parser')
                extracted_content = {}

                # Extract content using configured selectors
                for selector_name, selector in target['selectors'].items():
                    elements = soup.select(selector)
                    if elements:
                        text_parts = [elem.get_text(strip=True) for elem in elements]
                        extracted_content[selector_name] = ' '.join(text_parts)

                # Combine all extracted content
                combined_text = ' '.join(extracted_content.values())
                scraped_info = {
                    'url': url,
                    'content': sanitize_text(combined_text),
                    'selectors_found': list(extracted_content.keys())
                }

                result['scraped_data'][target['url']] = scraped_info

                # Cache the result
                save_json_cache(cache_file, scraped_info)
                logger.info(f"Scraped {len(combined_text)} characters from {url}")

            except requests.RequestException as e:
                error_msg = f"Failed to scrape {url}: {e}"
                logger.warning(error_msg)
                result['errors'].append(error_msg)

            except Exception as e:
                error_msg = f"Error parsing {url}: {e}"
                logger.error(error_msg)
                result['errors'].append(error_msg)

    except Exception as e:
        logger.error(f"Error in scrape_website: {e}")
        result['errors'].append(str(e))

    return result


def merge_data(local_data: Dict, web_data: Dict) -> str:
    """
    Merge local and web data into unified context string

    Args:
        local_data: Data from local files
        web_data: Data from web scraping

    Returns:
        str: Merged context text
    """
    context_parts = []

    # Add local file data
    context_parts.append("=== UNIVERSITY DATA FROM LOCAL FILES ===\n")

    if local_data.get('files_data'):
        for file_key, file_info in local_data['files_data'].items():
            context_parts.append(f"\n--- {file_info['filename']} ---\n")
            context_parts.append(file_info['content'])

    # Add web scraped data
    if web_data.get('scraped_data'):
        context_parts.append("\n\n=== LIVE DATA FROM UNIVERSITY WEBSITE ===\n")

        for url_path, scraped_info in web_data['scraped_data'].items():
            context_parts.append(f"\n--- From {scraped_info['url']} ---\n")
            context_parts.append(scraped_info['content'])

    merged_context = '\n'.join(context_parts)
    logger.info(f"Merged context: {len(merged_context)} characters total")

    return merged_context


@measure_execution_time
def get_complete_context(use_web_scraping: bool = True, use_cache: bool = True) -> Dict[str, any]:
    """
    Get complete context by loading local data and optionally scraping web

    Args:
        use_web_scraping: Whether to include web scraped data
        use_cache: Whether to use cached web data

    Returns:
        dict: {context, local_data, web_data, errors}
    """
    result = {
        'context': '',
        'local_data': {},
        'web_data': {},
        'errors': []
    }

    # Load local data
    local_result = load_local_data()
    result['local_data'] = local_result
    result['errors'].extend(local_result['errors'])

    # Load web data if enabled
    if use_web_scraping and SCRAPING_ENABLED:
        web_result = scrape_website(use_cache=use_cache)
        result['web_data'] = web_result
        result['errors'].extend(web_result['errors'])
    else:
        result['web_data'] = {'scraped_data': {}, 'errors': [], 'cached': False}

    # Merge all data
    result['context'] = merge_data(result['local_data'], result['web_data'])

    return result


if __name__ == '__main__':
    # Test the ingestion module
    logger.info("Testing data ingestion module...")

    # Test local data loading
    print("\n" + "="*60)
    print("Testing local data extraction...")
    print("="*60)
    local_data = load_local_data()
    print(f"Total files: {local_data['summary']['total_files']}")
    print(f"Successful: {local_data['summary']['successful']}")
    print(f"Failed: {local_data['summary']['failed']}")

    if local_data['files_data']:
        print("\nExtracted files:")
        for key, info in local_data['files_data'].items():
            print(f"  - {info['filename']}: {len(info['content'])} characters")

    # Test complete context
    print("\n" + "="*60)
    print("Getting complete context...")
    print("="*60)
    complete = get_complete_context(use_web_scraping=False)
    print(f"Total context length: {len(complete['context'])} characters")
    print(f"Errors: {len(complete['errors'])}")

    if complete['context']:
        print("\nContext preview (first 500 chars):")
        print(complete['context'][:500])
