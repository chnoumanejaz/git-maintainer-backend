import json
import re
from pathlib import Path
from openai import OpenAI
from pydantic import ValidationError
from commits.constants import API_KEY_DEEPSEEK
from commits.openai.openai_models import OpenAIResponse

def get_ai_client() -> OpenAI:
    """Returns a reusable OpenAI client instance."""
    return OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=API_KEY_DEEPSEEK
    )

def load_context(context_name: str) -> str:
    """Load system context from a given file inside the context directory."""
    CONTEXT_DIR = Path("commits/openai/contexts")
    print("CONTEXT_DIR: ", CONTEXT_DIR)
    context_file = CONTEXT_DIR / f"{context_name}.txt"

    if not context_file.exists():
        print(f"Warning: Context file '{context_name}.txt' not found. Using default empty context.")
        return ""

    with open(context_file, "r", encoding="utf-8") as file:
        return file.read().strip()


def get_ai_response(user_input: str, context_name: str) -> OpenAIResponse:
    """Get AI response using the specified context file."""
    system_context = load_context(context_name)
    client = get_ai_client()

    try:
        completion = client.chat.completions.create(
            extra_body={},
            model="deepseek/deepseek-r1-distill-llama-70b:free",
            messages=[
                {"role": "system", "content": system_context},
                {"role": "user", "content": user_input}
            ]
        )

        response_text = completion.choices[0].message.content.strip()
        print("Ai response_text:", response_text)

        # Extract JSON response
        match = re.search(r'\{.*\}', response_text, re.DOTALL)
        extracted_response = match.group(0) if match else "{}"

        response_dict = json.loads(extracted_response)
        return OpenAIResponse(**response_dict)

    except json.JSONDecodeError:
        print("Error: Failed to parse AI response JSON.")
        return OpenAIResponse(status="error", response="Invalid AI response format.")

    except ValidationError as e:
        print(f"Validation Error: {e}")
        return OpenAIResponse(status="error", response="Invalid AI response structure.")

    except Exception as e:
        print(f"Unexpected Error: {e}")
        return OpenAIResponse(status="error", response="An unexpected error occurred.")
