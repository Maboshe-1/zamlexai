# core/utils/llm.py

import requests
from requests.exceptions import ReadTimeout, RequestException

# Default model: dense Mistral 7 B
DEFAULT_MODEL = "mistral:latest"
OLLAMA_URL    = "http://localhost:11434/api/generate"
TIMEOUT       = 300  # seconds

def call_local_llm(prompt: str, model: str = None) -> str:
    """
    Send `prompt` to local Ollama HTTP API using the specified model (or default).
    Returns parsed JSON "response" or raw text. Returns warning on timeout or network error.

    Args:
        prompt (str): The text prompt for the LLM.
        model (str, optional): Ollama model name (e.g., "mistral:latest").
    """
    model_name = model or DEFAULT_MODEL
    try:
        resp = requests.post(
            OLLAMA_URL,
            json={
                "model":    model_name,
                "prompt":   prompt,
                "stream":   False
            },
            timeout=TIMEOUT
        )

        # Attempt JSON parsing
        try:
            data = resp.json()
            for key in ("response", "text", "choices"):
                if key in data:
                    if key == "choices" and isinstance(data[key], list):
                        return data[key][0].get("message", {}).get("content", "")
                    return data[key]
        except ValueError:
            # Not JSON: return raw text
            return resp.text

    except ReadTimeout:
        return (
            "⚠️ The language model took too long to respond "
            f"(> {TIMEOUT} seconds). Please try again or reduce prompt size."
        )
    except RequestException as e:
        return f"⚠️ Error communicating with the LLM: {e}"

    return resp.text or ""
