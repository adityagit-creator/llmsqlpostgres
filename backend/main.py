import sys
import os

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from backend.api.chatbot_routes import router as chatbot_router
import logging

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = FastAPI(
    title="LLM SQL Chatbot",
    description="A chatbot that translates natural language to SQL queries and executes them on PostgreSQL.",
    version="1.0.0",
)


origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "null", 
    "http://127.0.0.1:5500", 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.options("/{path:path}")
async def options_handler(request: Request, path: str):
    response = Response(status_code=200)
    response.headers["Access-Control-Allow-Origin"] = request.headers.get("Origin") or "*"
    response.headers["Access-Control-Allow-Methods"] = request.headers.get("Access-Control-Request-Method") or "*"
    response.headers["Access-Control-Allow-Headers"] = request.headers.get("Access-Control-Request-Headers") or "*"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Access-Control-Max-Age"] = "86400"
    return response
app.include_router(chatbot_router, prefix="/api")

@app.get("/")
async def read_root():
    return {"message": "Welcome to the LLM SQL Chatbot API!"}
