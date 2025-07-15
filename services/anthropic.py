import anthropic
from utils.model import ModelParameters

def calculate_price(input_tokens, output_tokens):
    return ((input_tokens/1000000) * 3) + (15 * (output_tokens/1000000)) 

# The Anthropic client automatically looks for the ANTHROPIC_API_KEY environment variable.
# Make sure it is set in your environment or a .env file.
try:
    client = anthropic.AsyncAnthropic()
except anthropic.AnthropicError as e:
    print(f"Failed to initialize Anthropic client: {e}")
    # This allows the server to start even if the key is missing.
    # Calls to this service will fail gracefully.
    client = None

async def call_anthropic_service(prompt: str, modelParameters: ModelParameters, model: str = "claude-3-sonnet-20240229") -> dict:
    """
    Makes an asynchronous call to the Anthropic API to get a chat completion.
    """
    if not client:
        return {
            "source": "anthropic",
            "error": "Anthropic client is not initialized. Check server logs and ANTHROPIC_API_KEY.",
        }

    try:
        # Use the recommended 'messages' API for newer models and a more consistent structure.
        response = await client.messages.create(
            model=model,
            max_tokens=1024,
            temperature=modelParameters.temperature,
            top_p=modelParameters.topP,
            messages=[
                {"role": "user", "content": prompt}
            ],
        )
        return {
            "source": "anthropic", 
            "content": response.content[0].text, 
            "token_usage": (response.usage.input_tokens + response.usage.output_tokens),
            "price": calculate_price(response.usage.input_tokens, response.usage.output_tokens)
        }
    except anthropic.APIError as e:
        # Handle API errors (e.g., invalid request, rate limits)
        return {"source": "anthropic", "error": f"Anthropic API Error: {e}"}
