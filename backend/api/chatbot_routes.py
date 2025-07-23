# llm-sql-chatbot/backend/api/chatbot_routes.py
# This module defines the API endpoints for the chatbot.
# ---
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
# Corrected import to be absolute relative to the 'backend' package
from backend.services.sql_agent import SQLAgent
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Create an API router
router = APIRouter()

# Initialize the SQLAgent
sql_agent = SQLAgent()

# Define a Pydantic model for the chat request body
class ChatRequest(BaseModel):
    message: str

@router.post("/chat")
async def chat_with_llm(request: ChatRequest): # Made async
    """
    API endpoint to send a natural language message to the chatbot
    and receive a SQL query result.
    """
    logging.info(f"Received chat request: {request.message}")
    try:
        # Process the natural language query using the SQLAgent
        response = await sql_agent.process_query(request.message) # Await the async call
        logging.info(f"Sending response back: {response}")
        return response
    except Exception as e:
        logging.error(f"Error in chat endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# --- END of api/chatbot_routes.py ---
