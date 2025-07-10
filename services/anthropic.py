import anthropic

# The Anthropic client automatically looks for the ANTHROPIC_API_KEY environment variable.
# Make sure it is set in your environment or a .env file.
try:
    client = anthropic.AsyncAnthropic()
except anthropic.AnthropicError as e:
    print(f"Failed to initialize Anthropic client: {e}")
    # This allows the server to start even if the key is missing.
    # Calls to this service will fail gracefully.
    client = None

async def call_anthropic_service(prompt: str) -> dict:
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
            model="claude-3-sonnet-20240229",  # A powerful and fast Claude 3 model
            max_tokens=1024,
            messages=[
                {"role": "user", "content": prompt}
            ],
        )
        return {"source": "anthropic", "content": response.content[0].text}
    except anthropic.APIError as e:
        # Handle API errors (e.g., invalid request, rate limits)
        return {"source": "anthropic", "error": f"Anthropic API Error: {e}"}
