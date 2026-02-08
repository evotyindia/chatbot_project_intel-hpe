"""
Gemini API Integration Module
Handles communication with Google Gemini 2.5 Flash model
IMPORTANT: Only accepts Scaledown-compressed prompts
"""

import google.generativeai as genai
from typing import List, Dict, Optional
from utils import logger, measure_execution_time
from config import (
    GEMINI_API_KEY,
    GEMINI_MODEL,
    GEMINI_TEMPERATURE,
    GEMINI_MAX_TOKENS,
    GEMINI_TOP_P,
    SYSTEM_INSTRUCTION
)


class GeminiClient:
    """
    Google Gemini API client for university admissions chatbot
    Generates responses from Scaledown-compressed prompts
    """

    def __init__(self, api_key: str = None, model_name: str = None):
        """
        Initialize Gemini client

        Args:
            api_key: Gemini API key (default: from config)
            model_name: Model name (default: from config)
        """
        self.api_key = api_key or GEMINI_API_KEY
        self.model_name = model_name or GEMINI_MODEL
        self.system_instruction = SYSTEM_INSTRUCTION

        if not self.api_key:
            logger.error("Gemini API key not configured!")
            raise ValueError("GEMINI_API_KEY must be set in environment variables")

        # Configure Gemini API
        genai.configure(api_key=self.api_key)

        # Initialize model
        self.model = genai.GenerativeModel(
            model_name=self.model_name,
            generation_config={
                'temperature': GEMINI_TEMPERATURE,
                'max_output_tokens': GEMINI_MAX_TOKENS,
                'top_p': GEMINI_TOP_P,
            }
        )

        logger.info(f"Gemini client initialized with model: {self.model_name}")

    @measure_execution_time
    def generate_response(
        self,
        compressed_prompt: str,
        conversation_history: Optional[List[Dict]] = None
    ) -> str:
        """
        Generate response from compressed prompt

        Args:
            compressed_prompt: Scaledown-compressed context + user query
            conversation_history: Optional list of previous exchanges
                                Format: [{'user': '...', 'assistant': '...'}, ...]

        Returns:
            str: Gemini's response
        """
        try:
            # Build full prompt with system instruction
            full_prompt = f"{self.system_instruction}\n\n{compressed_prompt}"

            # Add conversation history if provided
            if conversation_history:
                history_text = self._format_conversation_history(conversation_history)
                if history_text:
                    full_prompt = f"{full_prompt}\n\n{history_text}"

            logger.info(f"Generating Gemini response (prompt length: {len(full_prompt)} chars)...")

            # Generate response
            response = self.model.generate_content(full_prompt)

            # Extract text from response
            if response and response.text:
                response_text = response.text.strip()
                logger.info(f"Gemini response generated: {len(response_text)} characters")
                return response_text
            else:
                logger.warning("Gemini returned empty response")
                return "I apologize, but I couldn't generate a response. Please try rephrasing your question."

        except Exception as e:
            logger.error(f"Gemini API error: {str(e)}")
            return self._get_error_response(e)

    def _format_conversation_history(self, history: List[Dict], max_exchanges: int = 5) -> str:
        """
        Format conversation history for inclusion in prompt

        Args:
            history: List of conversation exchanges
            max_exchanges: Maximum number of recent exchanges to include

        Returns:
            str: Formatted conversation history
        """
        if not history:
            return ""

        # Take most recent exchanges
        recent_history = history[-max_exchanges:] if len(history) > max_exchanges else history

        formatted_parts = ["Previous Conversation:"]

        for exchange in recent_history:
            user_msg = exchange.get('user', '')
            assistant_msg = exchange.get('assistant', '')

            if user_msg:
                formatted_parts.append(f"User: {user_msg}")
            if assistant_msg:
                formatted_parts.append(f"Assistant: {assistant_msg}")

        return '\n'.join(formatted_parts)

    def _get_error_response(self, error: Exception) -> str:
        """
        Generate user-friendly error response

        Args:
            error: Exception that occurred

        Returns:
            str: User-friendly error message
        """
        error_str = str(error).lower()

        # Rate limit error
        if 'quota' in error_str or 'rate limit' in error_str:
            return ("I'm currently experiencing high demand. "
                   "Please try again in a moment.")

        # API key error
        if 'api key' in error_str or 'authentication' in error_str:
            return ("There's a configuration issue with the chatbot. "
                   "Please contact support.")

        # Content filtering
        if 'safety' in error_str or 'blocked' in error_str:
            return ("I can't respond to that type of question. "
                   "Please ask about university admissions, programs, or fees.")

        # Generic error
        return ("I'm having trouble processing your request right now. "
               "Please try again or rephrase your question.")

    @measure_execution_time
    def generate_streaming_response(
        self,
        compressed_prompt: str,
        conversation_history: Optional[List[Dict]] = None
    ):
        """
        Generate streaming response (for future implementation)

        Args:
            compressed_prompt: Scaledown-compressed context + user query
            conversation_history: Optional conversation history

        Yields:
            str: Response chunks
        """
        try:
            # Build full prompt
            full_prompt = f"{self.system_instruction}\n\n{compressed_prompt}"

            if conversation_history:
                history_text = self._format_conversation_history(conversation_history)
                if history_text:
                    full_prompt = f"{full_prompt}\n\n{history_text}"

            # Generate streaming response
            response = self.model.generate_content(full_prompt, stream=True)

            for chunk in response:
                if chunk.text:
                    yield chunk.text

        except Exception as e:
            logger.error(f"Gemini streaming error: {str(e)}")
            yield self._get_error_response(e)

    def is_configured(self) -> bool:
        """Check if Gemini client is properly configured"""
        return bool(self.api_key)


# Singleton instance
_gemini_instance = None


def get_gemini_client() -> GeminiClient:
    """Get singleton Gemini client instance"""
    global _gemini_instance
    if _gemini_instance is None:
        _gemini_instance = GeminiClient()
    return _gemini_instance


def generate_response(compressed_prompt: str, conversation_history: Optional[List[Dict]] = None) -> str:
    """
    Convenience function to generate response

    Args:
        compressed_prompt: Scaledown-compressed prompt
        conversation_history: Optional conversation history

    Returns:
        str: Generated response
    """
    client = get_gemini_client()
    return client.generate_response(compressed_prompt, conversation_history)


if __name__ == '__main__':
    # Test Gemini client
    logger.info("Testing Gemini client...")

    try:
        client = GeminiClient()

        if not client.is_configured():
            print("\n" + "="*60)
            print("ERROR: Gemini API key not configured!")
            print("Set GEMINI_API_KEY in your .env file")
            print("="*60)
        else:
            print("\n" + "="*60)
            print("Gemini Client Test")
            print("="*60)

            # Test prompt (simulating compressed output)
            test_prompt = """
            Context: University requires SAT minimum 1200, GPA 3.0, application fee $75.
Deadline: January 15.

            User Query: What is the application deadline?
            """

            print(f"Test prompt length: {len(test_prompt)} characters")
            print("\nGenerating response...")

            response = client.generate_response(test_prompt)

            print("\n" + "="*60)
            print("Response:")
            print("="*60)
            print(response)

            # Test with conversation history
            print("\n" + "="*60)
            print("Testing with conversation history...")
            print("="*60)

            history = [
                {
                    'user': 'What is the application deadline?',
                    'assistant': 'The application deadline is January 15.'
                }
            ]

            test_prompt_2 = """
            Context: Application fee is $75. Fee waivers available.

            User Query: How much is the application fee?
            """

            response_2 = client.generate_response(test_prompt_2, history)

            print("\nResponse with history:")
            print(response_2)

    except ValueError as e:
        print(f"\nConfiguration Error: {e}")
        print("Please set GEMINI_API_KEY in your .env file")
    except Exception as e:
        print(f"\nError: {e}")
