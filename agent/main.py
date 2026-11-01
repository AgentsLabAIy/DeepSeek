
from pathlib import Path

from agent.llm_invocation.invocation import invoke_llm


# ==================================================
# PATH CONFIGURATION
# ==================================================

AGENT_DIR = Path(__file__).resolve().parent

AGENT_CONFIG_PATH = AGENT_DIR / "agent.md"
SYSTEM_PROMPT_PATH = AGENT_DIR / "system" / "system_prompt.md"
SKILL_PATH = AGENT_DIR / "skills" / "skill.md"


# ==================================================
# FILE LOADING
# ==================================================

def load_file(file_path: Path) -> str:
    """
    Load a Markdown instruction file.
    """

    if not file_path.exists():
        raise FileNotFoundError(
            f"Required file not found: {file_path}"
        )

    return file_path.read_text(
        encoding="utf-8"
    ).strip()


def load_agent_context() -> dict:
    """
    Load agent configuration, system prompt,
    and available skills.
    """

    return {
        "agent": load_file(AGENT_CONFIG_PATH),
        "system_prompt": load_file(SYSTEM_PROMPT_PATH),
        "skill": load_file(SKILL_PATH)
    }


# ==================================================
# PROMPT CONSTRUCTION
# ==================================================

def build_messages(
    query: str,
    agent_context: dict
) -> list:
    """
    Construct messages for the Ollama Chat API.
    """

    system_message = f"""
{agent_context["system_prompt"]}

# AGENT CONFIGURATION

{agent_context["agent"]}

# AVAILABLE SKILLS

{agent_context["skill"]}
"""

    messages = [
        {
            "role": "system",
            "content": system_message.strip()
        },
        {
            "role": "user",
            "content": query
        }
    ]

    return messages


# ==================================================
# AGENT EXECUTION
# ==================================================

def run_agent(
    query: str,
    parameters: dict | None = None
) -> str:
    """
    Execute the agent.

    1. Load agent instructions.
    2. Construct messages.
    3. Invoke the LLM.
    4. Return the model response.
    """

    if not query or not query.strip():
        raise ValueError("Query cannot be empty.")

    agent_context = load_agent_context()

    messages = build_messages(
        query=query,
        agent_context=agent_context
    )

    response = invoke_llm(
        messages=messages,
        parameters=parameters
    )

    return response


# ==================================================
# APPLICATION ENTRY POINT
# ==================================================

def main():

    print("=" * 50)
    print("AGENT-01")
    print("=" * 50)

    query = input("\nEnter your query: ").strip()

    # Ollama generation parameters
    parameters = {
        "temperature": 0.6,
        "top_p": 0.9,
        "num_ctx": 8192
    }

    try:

        response = run_agent(
            query=query,
            parameters=parameters
        )

        print("\n" + "=" * 50)
        print("AGENT RESPONSE")
        print("=" * 50)

        print(response)

    except Exception as error:

        print("\nAgent execution failed:")
        print(error)


if __name__ == "__main__":
    main()
