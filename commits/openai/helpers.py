import json
import re
from pathlib import Path
from openai import OpenAI
from pydantic import ValidationError
from commits.constants import API_KEY_DEEPSEEK
from commits.openai.openai_models import OpenAIResponse
from commits.logger import Log as log

def get_ai_client() -> OpenAI:
    """Returns a reusable OpenAI client instance."""
    return OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=API_KEY_DEEPSEEK
    )

def load_context(context_name: str) -> str:
    """Load system context from a given file inside the context directory."""
    CONTEXT_DIR = Path("commits/openai/contexts")
    context_file = CONTEXT_DIR / f"{context_name}.txt"
    log.info(message=f"Loading context from '{context_file}'")

    if not context_file.exists():
        log.warning(message=f"Context file '{context_name}.txt' not found. Using default empty context.")
        return ""

    with open(context_file, "r", encoding="utf-8") as file:
        return file.read().strip()


def get_ai_response(user_input: str, context_name: str) -> OpenAIResponse:
    """Get AI response using the specified context file."""
    system_context = load_context(context_name)
    client = get_ai_client()

    try:
        log.info(message=f"User messsage: {user_input}")
        log.info(message="Sending AI request...")
        completion = client.chat.completions.create(
            extra_body={},
            model="deepseek/deepseek-r1-distill-llama-70b:free",
            messages=[
                {"role": "system", "content": system_context},
                {"role": "user", "content": user_input}
            ]
        )

        response_text = completion.choices[0].message.content.strip()
        log.log(message="Ai response_text:", data=response_text)

        # Extract JSON response
        match = re.search(r'\{.*\}', response_text, re.DOTALL)
        extracted_response = match.group(0) if match else "{}"

        response_dict = json.loads(extracted_response)
        log.info(message="AI response_dict:", data=response_dict, formatjson=True)
        return OpenAIResponse(**response_dict)

    except json.JSONDecodeError:
        log.error(message="Failed to parse AI response JSON.")
        return OpenAIResponse(status="error", response="Invalid AI response format.")

    except ValidationError as e:
        log.error(message=f"Validation Error: {e}")
        return OpenAIResponse(status="error", response="Invalid AI response structure.")

    except Exception as e:
        log.error(message=f"Unexpected Error: {e}")
        return OpenAIResponse(status="error", response="An unexpected error occurred.")
