import requests


OLLAMA_URL = "http://localhost:11434"
MODEL_NAME = "deepseek-r1:7b"


def invoke_llm(
    messages: list,
    parameters: dict | None = None
) -> str:

    payload = {
        "model": MODEL_NAME,
        "messages": messages,
        "stream": False,
        "options": parameters or {}
    }

    try:
        response = requests.post(
            f"{OLLAMA_URL}/api/chat",
            json=payload,
            timeout=300
        )

        response.raise_for_status()

        result = response.json()

        return result["message"]["content"]

    except requests.exceptions.RequestException as exc:
        raise RuntimeError(f"Ollama invocation failed: {exc}") from exc