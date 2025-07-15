from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from services.mongodb import connect_to_mongodb, get_mongodb_client
from utils.model import ANTHROPIC, OPENAI, XAI, ChatMessage, ChatRequest
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
connect_to_mongodb()

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
    if request.provider == OPENAI:
        return await call_openai_service(request.prompt, request.modelParameters, request.model)
    elif request.provider == ANTHROPIC:
        return await call_anthropic_service(request.prompt, request.modelParameters, request.model)
    elif request.provider == XAI:
        return await call_xai_service(request.prompt, request.modelParameters, request.model)

    # This path is technically unreachable due to Pydantic's `Literal`
    # validation, but it's good practice to handle it defensively.
    raise HTTPException(status_code=400, detail="Invalid provider specified.")

@app.post("/v1/chat/save")
async def save_chat(message: ChatMessage):
    try:
        mongoClient = get_mongodb_client()
        if(mongoClient is not None):
            db = mongoClient["llm-playground-data"]
            collection = db["llm-playground-collection"]
            result = collection.insert_one(message.data)
            return {"status": "success", "id": str(result.inserted_id)}
        else:
            print("Error - MongoClient is not defined")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    # This allows you to run the server directly with `python server.py`
    # The `reload=True` flag is for development, so the server restarts on code changes.
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)