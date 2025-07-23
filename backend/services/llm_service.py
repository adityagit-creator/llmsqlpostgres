# llm-sql-chatbot/backend/services/llm_service.py
# This module handles interactions with the Large Language Model (LLM).
# ---
import google.generativeai as genai
from config.settings import settings
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class LLMService:
    """
    Service for interacting with the Google Gemini LLM.
    """
    def __init__(self):
        # Configure the Google Generative AI client with the API key
        genai.configure(api_key=settings.GOOGLE_API_KEY)
        # Initialize the Gemini model
        self.model = genai.GenerativeModel('gemini-2.0-flash')
        logging.info("LLMService initialized with Gemini 2.0 Flash model.")

    async def generate_text(self, prompt: str) -> str: # Made async
        """
        Generates text using the LLM based on the given prompt.
        """
        try:
            # Use generate_content_async for asynchronous calls
            response = await self.model.generate_content_async(prompt)
            generated_text = response.text
            logging.info(f"LLM generated response for prompt: '{prompt[:50]}...'")
            return generated_text
        except Exception as e:
            logging.error(f"Error generating text with LLM: {e}")
            raise RuntimeError(f"LLM generation failed: {e}")

# --- END of services/llm_service.py ---
