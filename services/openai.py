import openai
import os

from utils.model import ModelParameters

def calculate_price(input_tokens, output_tokens):
    return ((input_tokens/1000000) * 0.15) + (0.60 * (output_tokens/1000000)) 

# Initialize the OpenAI client
try:
    client = openai.AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
except Exception as e:
    print(f"Failed to initialize OpenAI client: {e}")
    client = None

async def call_openai_service(prompt: str, modelParameters: ModelParameters, model: str="gpt-4o-mini") -> dict:
    """
    Makes an asynchronous call to the OpenAI API to get a chat completion.
    """
    if not client:
        return {
            "source": "openai",
            "error": "OpenAI client is not initialized. Check OPENAI_API_KEY.",
        }

    try:
        response = await client.chat.completions.create(
            model=model,
            temperature=modelParameters.temperature,
            top_p=modelParameters.top_p,
            messages=[{"role": "user", "content": prompt}],
        )
        return {
            "source": "openai",
            "content": response.choices[0].message.content,
            "token_usage": response.usage.total_tokens,
            "price": calculate_price(response.usage.prompt_tokens, response.usage.completion_tokens)
        }
    except openai.APIStatusError as e:
        # Catch specific API errors
        return {
            "source": "openai",
            "error": f"OpenAI API Error: {e.message} (Status: {e.status_code})"
        }
    except Exception as e:
        # Catch other exceptions
        return {
            "source": "openai",
            "error": f"Unexpected error: {str(e)}"
        }