from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.services.sql_agent import SQLAgent
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

router = APIRouter()
sql_agent = SQLAgent()

class ChatRequest(BaseModel):
    message: str

@router.post("/chat")
async def chat_with_llm(request: ChatRequest): 
    logging.info(f"Received chat request: {request.message}")
    try:
        response = await sql_agent.process_query(request.message) 
        logging.info(f"Sending response back: {response}")
        return response
    except Exception as e:
        logging.error(f"Error in chat endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))
