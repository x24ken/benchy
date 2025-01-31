import pytest
from modules.fireworks_llm import bench_prompt, text_prompt, thought_prompt

@pytest.fixture
def model():
    return "accounts/fireworks/models/llama-v3p2-3b-instruct"

def test_bench_prompt(model):
    prompt = "Hello, how are you?"
    response = bench_prompt(prompt, model)
    assert response is not None
    assert hasattr(response, "response")
    print("bench_prompt response:", response.response)

def test_text_prompt(model):
    prompt = "Please summarize the following text: Fireworks testing is in progress."
    response = text_prompt(prompt, model)
    assert response is not None
    assert hasattr(response, "response")
    print("text_prompt response:", response.response)

def test_thought_prompt(model):
    prompt = "Give me your internal thought process about fireworks testing."
    response = thought_prompt(prompt, model)
    assert response is not None
    assert hasattr(response, "response")
    assert hasattr(response, "thoughts")
    print("thought_prompt response:", response.response)
    print("thought_prompt thoughts:", response.thoughts)
