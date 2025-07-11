from typing import Optional, Literal
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import uvicorn

# Import the service functions
from services.openai import call_openai_service
from services.anthropic import call_anthropic_service
from services.xai import call_xai_service

# Load environment variables from a .env file
load_dotenv()

# Initialize the FastAPI app
# This instance will be the main point of interaction to create all your API.
app = FastAPI(
    title="FastAPI Server",
    description="A basic template for a FastAPI server.",
    version="0.1.0",
)

# Mongo DB Client
uri = "mongodb+srv://awaiskamran:_CrrfQZTZ$6$Y-P@llm-playground.4a1zyij.mongodb.net/?retryWrites=true&w=majority&appName=llm-playground"
mongoClient = MongoClient(uri, server_api=ServerApi('1'))
try:
    mongoClient.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

# Define allowed origins for CORS
origins = [
    "http://localhost:8080",
    "https://triple-chat-echo.vercel.app",
]

# Add CORS middleware to the application
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Data Models
class ChatRequest(BaseModel):
    """Defines the request body for the chat endpoint."""
    prompt: str
    provider: Literal["openai", "anthropic", "xai"]


@app.get("/health")
async def read_root():
    """
    A simple root endpoint to confirm the server is running.
    """
    return {"message": "Do you really wanan Build That Idea?"}

@app.post("/v1/chat/completions")
async def create_completion(request: ChatRequest):
    """
    This endpoint receives a prompt and a provider, and forwards the request
    to the specified AI service. It returns the response from that service.
    """
    if request.provider == "openai":
        return await call_openai_service(request.prompt)
    elif request.provider == "anthropic":
        return await call_anthropic_service(request.prompt)
    elif request.provider == "xai":
        return await call_xai_service(request.prompt)

    # This path is technically unreachable due to Pydantic's `Literal`
    # validation, but it's good practice to handle it defensively.
    raise HTTPException(status_code=400, detail="Invalid provider specified.")


# if __name__ == "__main__":
#     # This allows you to run the server directly with `python server.py`
#     # The `reload=True` flag is for development, so the server restarts on code changes.
#     uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)