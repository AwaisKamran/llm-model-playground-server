import os
import grpc
from utils.model import ModelParameters
from xai_sdk import AsyncClient
from xai_sdk.chat import system, user

def calculate_price(input_tokens, output_tokens):
    return ((input_tokens/1000000)*3) + (15 * (output_tokens/1000000)) 

async def call_xai_service(prompt: str, modelParameters: ModelParameters, model: str = "grok-3"):
    """
    Async call to xAI Grok; returns:
      - {"source": "xai", "content": "..."} on success
      - {"source": "xai", "error": "..."} on failure
    """
    api_key = os.getenv("XAI_API_KEY")
    if not api_key:
        return {"source": "xai", "error": "Missing XAI_API_KEY environment variable."}

    client = AsyncClient(api_key=api_key)
    chat = client.chat.create(
        model=model,
        temperature=modelParameters.temperature,
        top_p=modelParameters.top_p,
        messages=[system("You are Grok."), user(prompt)]
    )

    try:
        response = await chat.sample()
        print(response)
        return {
            "source": "xai", 
            "content": response.content, 
            "token_usage": response.usage.total_tokens, 
            "price": calculate_price(response.usage.prompt_tokens, response.usage.completion_tokens)
        }

    except grpc.aio.AioRpcError as e:
        code = e.code().name if hasattr(e, "code") else "UNKNOWN"
        details = e.details() if hasattr(e, "details") else str(e)
        return {"source": "xai", "error": f"xAI API Error: {details} (Status: {code})"}

    except Exception as e:
        return {"source": "xai", "error": f"Unexpected error: {e}"}