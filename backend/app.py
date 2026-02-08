"""
Flask Application for University Admissions Chatbot
Main server that orchestrates data ingestion, compression, and AI response generation
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from typing import Dict, List
import sys
from pathlib import Path

# Add backend directory to path
sys.path.insert(0, str(Path(__file__).parent))

from config import FLASK_HOST, FLASK_PORT, FLASK_DEBUG, validate_config, print_config
from utils import logger, create_error_response, create_success_response
from ingest import get_complete_context
from scaledown import compress_context
from gemini_client import generate_response

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend access

# Global context cache (loaded once at startup)
_global_context_cache = None
_compressed_context_cache = None  # Cache for compressed context


def load_global_context() -> str:
    """
    Load and cache the complete university data context
    This is loaded once at startup to avoid repeated file I/O

    Returns:
        str: Merged context from all data sources
    """
    global _global_context_cache

    if _global_context_cache is None:
        logger.info("Loading global context from data sources...")

        # Get complete context (local files + optional web scraping)
        result = get_complete_context(use_web_scraping=True, use_cache=True)

        if result['context']:
            _global_context_cache = result['context']
            logger.info(f"Global context loaded: {len(_global_context_cache)} characters")

            if result['errors']:
                logger.warning(f"Context loaded with {len(result['errors'])} errors: {result['errors']}")
        else:
            logger.error("Failed to load global context")
            _global_context_cache = ""

    return _global_context_cache


@app.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint
    Returns server status and configuration info

    Returns:
        JSON: Server health status
    """
    try:
        context_loaded = _global_context_cache is not None
        context_size = len(_global_context_cache) if context_loaded else 0

        health_status = {
            'status': 'healthy',
            'context_loaded': context_loaded,
            'context_size_chars': context_size,
            'components': {
                'data_ingestion': context_loaded,
                'scaledown': True,  # Always available (has fallback)
                'gemini': True  # Checked at initialization
            }
        }

        return jsonify(health_status), 200

    except Exception as e:
        logger.error(f"Health check error: {e}")
        return jsonify({
            'status': 'unhealthy',
            'error': str(e)
        }), 500


@app.route('/chat', methods=['POST'])
def chat():
    """
    Main chatbot endpoint
    Receives user query, compresses context+query via Scaledown, sends to Gemini

    Request JSON:
        {
            "message": str (user query),
            "history": list (optional conversation history)
        }

    Response JSON:
        {
            "response": str (chatbot response),
            "compression_stats": dict (Scaledown compression statistics),
            "error": bool
        }
    """
    global _compressed_context_cache

    try:
        # Parse request
        data = request.get_json()

        if not data:
            return jsonify(create_error_response("Invalid JSON request", "INVALID_JSON")), 400

        user_message = data.get('message', '').strip()
        conversation_history = data.get('history', [])

        if not user_message:
            return jsonify(create_error_response("Message cannot be empty", "EMPTY_MESSAGE")), 400

        logger.info(f"Received chat request: '{user_message[:100]}...'")

        # Step 1: Load context (from cache)
        context = load_global_context()

        if not context:
            logger.error("No context available")
            return jsonify(create_error_response(
                "Chatbot context not available. Please try again later.",
                "NO_CONTEXT"
            )), 500

        logger.info(f"Using context: {len(context)} characters")

        # Step 2: Compress context + user query via Scaledown (with caching)
        logger.info("Preparing compressed prompt...")

        # Check if we have cached compressed context
        if _compressed_context_cache is None:
            logger.info("No cached compression found. Compressing full context via Scaledown...")
            compression_result = compress_context(
                context=context,
                prompt=user_message
            )

            # Cache the compression result for future requests
            if compression_result.get('successful', False):
                _compressed_context_cache = compression_result
                logger.info("Compressed context cached for future requests")
        else:
            logger.info("Using cached compressed context (faster response)")
            # Reuse cached compression with new prompt
            # Note: This is a simplified approach. For best results, we'd need to
            # re-compress with the new prompt, but this provides significant speed improvement
            compression_result = _compressed_context_cache.copy()
            # Append new user query to cached compressed context
            compression_result['compressed_prompt'] = f"{_compressed_context_cache['compressed_prompt']}\n\nNew User Query: {user_message}"

        if compression_result.get('error') and _compressed_context_cache is None:
            logger.warning(f"Scaledown compression failed: {compression_result['error']} - using fallback")

        compressed_prompt = compression_result['compressed_prompt']

        # Log compression statistics
        compression_stats = {
            'original_tokens': compression_result.get('original_tokens', 0),
            'compressed_tokens': compression_result.get('compressed_tokens', 0),
            'compression_ratio': compression_result.get('compression_ratio', 1.0),
            'successful': compression_result.get('successful', False),
            'latency_ms': compression_result.get('latency_ms', 0),
            'cached': _compressed_context_cache is not None
        }

        logger.info(f"Compression stats: {compression_stats}")

        # Step 3: Generate response using Gemini
        logger.info("Generating response with Gemini...")

        try:
            response_text = generate_response(
                compressed_prompt=compressed_prompt,
                conversation_history=conversation_history
            )

            logger.info(f"Response generated: {len(response_text)} characters")

            # Return success response
            return jsonify({
                'response': response_text,
                'compression_stats': compression_stats,
                'error': False
            }), 200

        except Exception as gemini_error:
            logger.error(f"Gemini generation error: {gemini_error}")
            return jsonify(create_error_response(
                "Failed to generate response. Please try again.",
                "GEMINI_ERROR"
            )), 500

    except Exception as e:
        logger.error(f"Chat endpoint error: {e}")
        return jsonify(create_error_response(
            "An unexpected error occurred. Please try again.",
            "INTERNAL_ERROR"
        )), 500


@app.route('/reload-context', methods=['POST'])
def reload_context():
    """
    Reload the global context from data sources
    Useful for updating data without restarting server

    Returns:
        JSON: Reload status
    """
    try:
        global _global_context_cache, _compressed_context_cache
        _global_context_cache = None
        _compressed_context_cache = None  # Clear compressed cache too

        # Force reload
        context = load_global_context()

        return jsonify({
            'success': True,
            'message': 'Context reloaded successfully',
            'context_size_chars': len(context)
        }), 200

    except Exception as e:
        logger.error(f"Reload context error: {e}")
        return jsonify(create_error_response(
            "Failed to reload context",
            "RELOAD_ERROR"
        )), 500


@app.route('/', methods=['GET'])
def index():
    """
    Root endpoint - API information

    Returns:
        JSON: API information
    """
    return jsonify({
        'service': 'University Admissions Chatbot API',
        'version': '1.0.0',
        'endpoints': {
            'GET /': 'API information',
            'GET /health': 'Health check',
            'POST /chat': 'Chat endpoint (send message)',
            'POST /reload-context': 'Reload university data context'
        },
        'documentation': 'See README.md for usage instructions'
    }), 200


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify(create_error_response("Endpoint not found", "NOT_FOUND")), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"Internal server error: {error}")
    return jsonify(create_error_response("Internal server error", "INTERNAL_ERROR")), 500


def initialize_app():
    """
    Initialize the application
    Validate configuration and load initial data
    """
    print("\n" + "="*60)
    print("UNIVERSITY ADMISSIONS CHATBOT - STARTING")
    print("="*60)

    # Validate configuration
    config_errors = validate_config()

    if config_errors:
        print("\n[ERROR] Configuration Errors:")
        for error in config_errors:
            print(f"  - {error}")
        print("\nPlease check your .env file and ensure all required variables are set.")
        print("See .env.example for reference.")
        sys.exit(1)

    print("\n[OK] Configuration validated")

    # Print configuration summary
    print_config()

    # Pre-load context
    print("\n" + "="*60)
    print("LOADING UNIVERSITY DATA")
    print("="*60)

    context = load_global_context()

    if context:
        print(f"\n[OK] Context loaded successfully")
        print(f"   Size: {len(context)} characters")
    else:
        print("\n[WARNING] No context loaded")
        print("   Chatbot will have limited functionality")

    print("\n" + "="*60)
    print("SERVER READY")
    print("="*60)
    print(f"Listening on http://{FLASK_HOST}:{FLASK_PORT}")
    print("Press CTRL+C to stop")
    print("="*60 + "\n")


if __name__ == '__main__':
    # Initialize and start the app
    initialize_app()

    # Run Flask server
    app.run(
        host=FLASK_HOST,
        port=FLASK_PORT,
        debug=FLASK_DEBUG
    )
