"""
Scaledown API Integration Module
Handles compression of context and prompts before sending to Gemini
CRITICAL: All data MUST be compressed via Scaledown before reaching Gemini
"""

import requests
import json
from typing import Dict, Optional
from utils import logger, format_compression_stats, measure_execution_time
from config import (
    SCALEDOWN_API_URL,
    SCALEDOWN_API_KEY,
    SCALEDOWN_RATE,
    SCALEDOWN_MODEL,
    SCALEDOWN_TIMEOUT
)


class ScaledownCompressor:
    """
    Scaledown API compression client
    Compresses context and prompts to reduce token usage
    """

    def __init__(self, api_key: str = None, api_url: str = None):
        """
        Initialize Scaledown compressor

        Args:
            api_key: Scaledown API key (default: from config)
            api_url: Scaledown API URL (default: from config)
        """
        self.api_key = api_key or SCALEDOWN_API_KEY
        self.api_url = api_url or SCALEDOWN_API_URL
        self.default_model = SCALEDOWN_MODEL
        self.default_rate = SCALEDOWN_RATE
        self.timeout = SCALEDOWN_TIMEOUT

        if not self.api_key:
            logger.warning("Scaledown API key not configured - compression will be skipped")

    @measure_execution_time
    def compress(
        self,
        context: str,
        prompt: str,
        model: str = None,
        rate: str = None
    ) -> Dict[str, any]:
        """
        Compress context and prompt using Scaledown API

        Args:
            context: Background context/knowledge to compress
            prompt: User query/prompt to compress
            model: Target model for compression (default: from config)
            rate: Compression rate ('auto' or specific value)

        Returns:
            dict: {
                'compressed_prompt': str,
                'original_tokens': int,
                'compressed_tokens': int,
                'compression_ratio': float,
                'successful': bool,
                'error': str or None,
                'latency_ms': int
            }
        """
        result = {
            'compressed_prompt': '',
            'original_tokens': 0,
            'compressed_tokens': 0,
            'compression_ratio': 1.0,
            'successful': False,
            'error': None,
            'latency_ms': 0
        }

        # Fallback if API key not configured
        if not self.api_key:
            logger.warning("Scaledown API key not configured - returning uncompressed prompt")
            result['compressed_prompt'] = f"{context}\n\nUser Query: {prompt}"
            result['error'] = "API key not configured"
            return result

        try:
            # Prepare request
            headers = {
                'x-api-key': self.api_key,
                'Content-Type': 'application/json'
            }

            payload = {
                'context': context,
                'prompt': prompt,
                'model': model or self.default_model,
                'scaledown': {
                    'rate': rate or self.default_rate
                }
            }

            logger.info(f"Compressing {len(context)} chars context + {len(prompt)} chars prompt...")

            # Make API request
            response = requests.post(
                self.api_url,
                headers=headers,
                data=json.dumps(payload),
                timeout=self.timeout
            )

            # Check response status
            response.raise_for_status()

            # Parse response
            data = response.json()

            # Extract compression results from correct structure
            # Scaledown API returns: {"results": {...}, "total_original_tokens": N, ...}
            results = data.get('results', {})

            result['compressed_prompt'] = results.get('compressed_prompt', '')
            result['original_tokens'] = data.get('total_original_tokens', 0)
            result['compressed_tokens'] = data.get('total_compressed_tokens', 0)
            result['latency_ms'] = data.get('latency_ms', 0)
            result['successful'] = data.get('successful', False)

            # Calculate compression ratio
            if result['original_tokens'] > 0 and result['compressed_tokens'] > 0:
                result['compression_ratio'] = result['original_tokens'] / result['compressed_tokens']
            else:
                # Estimate based on character count
                if result['compressed_prompt']:
                    original_length = len(context) + len(prompt)
                    compressed_length = len(result['compressed_prompt'])
                    result['compression_ratio'] = original_length / compressed_length if compressed_length > 0 else 1.0

            # Log statistics
            stats_str = format_compression_stats(result)
            logger.info(f"Scaledown compression completed: {stats_str}")

            if not result['successful']:
                logger.warning("Scaledown API returned successful=False")

        except requests.exceptions.Timeout:
            error_msg = f"Scaledown API timeout after {self.timeout}s"
            logger.error(error_msg)
            result['error'] = error_msg
            result['compressed_prompt'] = f"{context}\n\nUser Query: {prompt}"

        except requests.exceptions.HTTPError as e:
            error_msg = f"Scaledown API HTTP error: {e.response.status_code} - {e.response.text}"
            logger.error(error_msg)
            result['error'] = error_msg
            result['compressed_prompt'] = f"{context}\n\nUser Query: {prompt}"

        except requests.exceptions.RequestException as e:
            error_msg = f"Scaledown API request failed: {str(e)}"
            logger.error(error_msg)
            result['error'] = error_msg
            result['compressed_prompt'] = f"{context}\n\nUser Query: {prompt}"

        except json.JSONDecodeError as e:
            error_msg = f"Failed to parse Scaledown API response: {str(e)}"
            logger.error(error_msg)
            result['error'] = error_msg
            result['compressed_prompt'] = f"{context}\n\nUser Query: {prompt}"

        except Exception as e:
            error_msg = f"Unexpected error in Scaledown compression: {str(e)}"
            logger.error(error_msg)
            result['error'] = error_msg
            result['compressed_prompt'] = f"{context}\n\nUser Query: {prompt}"

        return result

    def is_configured(self) -> bool:
        """Check if Scaledown API is properly configured"""
        return bool(self.api_key)


# Singleton instance for easy access
_compressor_instance = None


def get_compressor() -> ScaledownCompressor:
    """Get singleton Scaledown compressor instance"""
    global _compressor_instance
    if _compressor_instance is None:
        _compressor_instance = ScaledownCompressor()
    return _compressor_instance


def compress_context(context: str, prompt: str, model: str = None) -> Dict[str, any]:
    """
    Convenience function to compress context and prompt

    Args:
        context: Background context to compress
        prompt: User query to compress
        model: Target model for compression

    Returns:
        dict: Compression result with compressed_prompt
    """
    compressor = get_compressor()
    return compressor.compress(context, prompt, model)


if __name__ == '__main__':
    # Test the Scaledown module
    logger.info("Testing Scaledown compression module...")

    compressor = ScaledownCompressor()

    if not compressor.is_configured():
        print("\n" + "="*60)
        print("WARNING: Scaledown API key not configured!")
        print("Set SCALEDOWN_API_KEY in your .env file to test compression")
        print("="*60)
        print("\nTesting fallback behavior (uncompressed)...")

    # Test with sample data
    sample_context = """
    University Admissions Information:
    - Application deadline: January 15
    - Required documents: Transcript, SAT scores, Essay
    - Minimum GPA: 3.0
    - Application fee: $75
    """

    sample_prompt = "What is the application deadline?"

    print("\n" + "="*60)
    print("Test Compression")
    print("="*60)
    print(f"Context length: {len(sample_context)} characters")
    print(f"Prompt length: {len(sample_prompt)} characters")

    result = compressor.compress(sample_context, sample_prompt)

    print(f"\nCompression successful: {result['successful']}")
    print(f"Original tokens: {result['original_tokens']}")
    print(f"Compressed tokens: {result['compressed_tokens']}")
    print(f"Compression ratio: {result['compression_ratio']:.2f}x")
    print(f"Latency: {result['latency_ms']} ms")

    if result['error']:
        print(f"Error: {result['error']}")

    print(f"\nCompressed prompt length: {len(result['compressed_prompt'])} characters")
    print("\nCompressed prompt preview:")
    print(result['compressed_prompt'][:300] + "..." if len(result['compressed_prompt']) > 300 else result['compressed_prompt'])
