from openai import OpenAI
from utils import timeit
from modules.data_types import BenchPromptResponse
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize DeepSeek client
client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

def bench_prompt(prompt: str, model: str) -> BenchPromptResponse:
    """
    Send a prompt to DeepSeek and get detailed benchmarking response.
    """
    try:
        with timeit() as t:
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                stream=False
            )
            elapsed_ms = t()

        return BenchPromptResponse(
            response=response.choices[0].message.content,
            tokens_per_second=0.0,  # DeepSeek doesn't provide this info
            provider="deepseek",
            total_duration_ms=elapsed_ms,
            load_duration_ms=0.0,
        )
    except Exception as e:
        print(f"DeepSeek error: {str(e)}")
        return BenchPromptResponse(
            response=f"Error: {str(e)}",
            tokens_per_second=0.0,
            provider="deepseek",
            total_duration_ms=0.0,
            load_duration_ms=0.0,
            errored=True,
        )
