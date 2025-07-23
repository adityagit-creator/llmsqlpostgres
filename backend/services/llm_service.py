import google.generativeai as genai
from config.settings import settings
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class LLMService:
    def __init__(self):
        genai.configure(api_key=settings.GOOGLE_API_KEY)
        self.model = genai.GenerativeModel('gemini-2.0-flash')
        logging.info("LLMService initialized with Gemini 2.0 Flash model.")

    async def generate_text(self, prompt: str) -> str: 
        try:
            response = await self.model.generate_content_async(prompt)
            generated_text = response.text
            logging.info(f"LLM generated response for prompt: '{prompt[:50]}...'")
            return generated_text
        except Exception as e:
            logging.error(f"Error generating text with LLM: {e}")
            raise RuntimeError(f"LLM generation failed: {e}")
