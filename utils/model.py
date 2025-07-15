from pydantic import BaseModel
from typing import Literal

OPENAI = "openai"
ANTHROPIC = "anthropic"
XAI = "xai"

class ModelParameters(BaseModel):
    temperature: float 
    topP: float

class ChatRequest(BaseModel):
    """Defines the request body for the chat endpoint."""
    prompt: str
    provider: Literal[OPENAI, ANTHROPIC, XAI]
    modelParameters: ModelParameters
    model: str
    
class ChatMessage(BaseModel):
    data: dict 
