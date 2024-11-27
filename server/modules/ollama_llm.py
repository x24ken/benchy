from ollama import chat
from modules.data_types import PromptResponse
from utils import timeit


def text_prompt(prompt: str, model: str) -> PromptResponse:
    """
    Send a prompt to Ollama and get a response.
    """
    try:
        with timeit() as t:
            response = chat(
                model=model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    },
                ],
            )
            elapsed_ms = t()

        return PromptResponse(
            response=response.message.content,
            runTimeMs=elapsed_ms,  # Now using actual timing
            inputAndOutputCost=0.0  # Ollama is free
        )
    except Exception as e:
        print(f"Ollama error: {str(e)}")
        return PromptResponse(
            response=f"Error: {str(e)}", runTimeMs=0, inputAndOutputCost=0.0
        )


def get_ollama_costs() -> tuple[int, int]:
    """
    Return token costs for Ollama (always 0 since it's free)
    """
    return 0, 0
