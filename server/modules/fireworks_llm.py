import os
import requests
import json

from modules.data_types import (
    BenchPromptResponse,
    PromptResponse,
    ThoughtResponse,
)

FIREWORKS_API_KEY = os.getenv("FIREWORKS_AI_API_KEY", "")

API_URL = "https://api.fireworks.ai/inference/v1/completions"

def get_fireworks_cost(model: str, input_tokens: int, output_tokens: int) -> float:
    # For now, just return 0.0 or substitute a real cost calculation if available
    return 0.0

def bench_prompt(prompt: str, model: str) -> BenchPromptResponse:
    import time
    start_time = time.time()
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {FIREWORKS_API_KEY}",
    }
    payload = {
        "model": model,
        "max_tokens": 20480,
        "prompt": prompt
    }

    response = requests.post(API_URL, headers=headers, data=json.dumps(payload))
    end_time = time.time()

    # Adjust these fields according to the actual Fireworks response shape
    resp_json = response.json()
    completions = resp_json.get("completions", [])
    content = completions[0].get("text", "") if completions else response.text

    # Build and return BenchPromptResponse
    return BenchPromptResponse(
        response=content,
        tokens_per_second=0.0,  # or compute if available
        provider="fireworks",
        total_duration_ms=(end_time - start_time) * 1000,
        load_duration_ms=0.0,
        errored=not response.ok
    )

def text_prompt(prompt: str, model: str) -> PromptResponse:
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {FIREWORKS_API_KEY}",
    }
    payload = {
        "model": model,
        "max_tokens": 20480,
        "prompt": prompt
    }

    response = requests.post(API_URL, headers=headers, data=json.dumps(payload))
    resp_json = response.json()
    completions = resp_json.get("completions", [])
    content = completions[0].get("text", "") if completions else response.text

    return PromptResponse(
        response=content,
        runTimeMs=0,  # or compute if desired
        inputAndOutputCost=0.0,  # or compute if you have cost details
    )

def thought_prompt(prompt: str, model: str) -> ThoughtResponse:
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {FIREWORKS_API_KEY}",
    }
    payload = {
        "model": model,
        "max_tokens": 20480,
        "prompt": prompt
    }

    response = requests.post(API_URL, headers=headers, data=json.dumps(payload))
    resp_json = response.json()
    completions = resp_json.get("completions", [])
    content = completions[0].get("text", "") if completions else response.text

    return ThoughtResponse(
        thoughts="",  # Fireworks doesn't appear to return chain-of-thought
        response=content,
        error=None if response.ok else content
    )
