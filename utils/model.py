from pydantic import BaseModel, Field
from typing import Literal, Optional

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
    model: Optional[str] = Field(
        None,
        description="Specify a model override, e.g., 'gpt-4o-mini | claude-3-sonnet-20240229 | grok-3'"
    )
    
class ChatMessage(BaseModel):
    data: dict 
