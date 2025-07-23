# llm-sql-chatbot/backend/main.py
# This is the main entry point for the FastAPI application.
# ---
import sys
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Ensure absolute imports work by adding project root to sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from backend.api.chatbot_routes import router as chatbot_router
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize the FastAPI application
app = FastAPI(
    title="LLM SQL Chatbot",
    description="A chatbot that translates natural language to SQL queries and executes them on PostgreSQL.",
    version="1.0.0",
)

# Configure CORS middleware
origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "null",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the chatbot API routes
app.include_router(chatbot_router, prefix="/api")

@app.get("/")
async def read_root():
    """
    Root endpoint for basic health check.
    """
    return {"message": "Welcome to the LLM SQL Chatbot API!"}

# --- END of main.py ---
