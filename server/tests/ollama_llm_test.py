import pytest
from modules.ollama_llm import text_prompt

def test_ollama_text_prompt():
    response = text_prompt("ping", "llama3.2:1b")
    assert response.response != ""
    assert response.runTimeMs > 0  # Now checking that timing is captured
    assert response.inputAndOutputCost == 0.0

def test_qwen_text_prompt():
    response = text_prompt("ping", "qwen2.5-coder:14b")
    assert response.response != ""
    assert response.runTimeMs > 0
    assert response.inputAndOutputCost == 0.0

def test_qwq_text_prompt():
    response = text_prompt("ping", "qwq:32b")
    assert response.response != ""
    assert response.runTimeMs > 0
    assert response.inputAndOutputCost == 0.0

def test_llama_3_2_latest_text_prompt():
    response = text_prompt("ping", "llama3.2:latest")
    assert response.response != ""
    assert response.runTimeMs > 0
    assert response.inputAndOutputCost == 0.0
