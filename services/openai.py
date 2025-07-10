import openai
import os

# Set API key (optional if already set in environment or .env file)
# openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize the OpenAI client
try:
    client = openai.AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
except Exception as e:
    print(f"Failed to initialize OpenAI client: {e}")
    client = None

async def call_openai_service(prompt: str) -> dict:
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
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
        )
        return {
            "source": "openai",
            "content": response.choices[0].message.content,
            "token_usage": response.usage.total_tokens
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