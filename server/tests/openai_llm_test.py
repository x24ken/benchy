import pytest
from modules.openai_llm import tool_prompt
from modules.tools import all_tools_list
from modules.data_types import ToolCallResponse, SimpleToolCall
import json
import types


@pytest.mark.parametrize(
    "prompt,expected_tool_calls,model",
    [
        (
            "Write code in main.py. Git commit it. Then document changes in README.md",
            [
                SimpleToolCall(tool_name="run_coder_agent", params={}),
                SimpleToolCall(tool_name="run_git_agent", params={}),
                SimpleToolCall(tool_name="run_docs_agent", params={}),
            ],
            "gpt-4o",
        ),
        (
            "Write some code for me in main.py, and then commit it to git",
            [
                SimpleToolCall(tool_name="run_coder_agent", params={}),
                SimpleToolCall(tool_name="run_git_agent", params={}),
            ],
            "gpt-4o",
        ),
        (
            "Document our latest feature",
            [SimpleToolCall(tool_name="run_docs_agent", params={})],
            "gpt-4o-mini",
        ),
    ],
)
def test_tool_prompt(
    prompt: str, expected_tool_calls: list[SimpleToolCall], model: str
):
    result = tool_prompt(prompt=prompt, model=model, force_tools=all_tools_list)

    # Verify response type and fields
    assert isinstance(result.tool_calls, list)
    assert isinstance(result.runTimeMs, int)
    assert isinstance(result.inputAndOutputCost, float)

    # Verify tool calls match exactly in order
    assert len(result.tool_calls) == len(expected_tool_calls)
    for actual, expected in zip(result.tool_calls, expected_tool_calls):
        assert actual.tool_name == expected.tool_name
        assert isinstance(actual.params, dict)
        assert len(actual.params) > 0  # Just verify params exist and aren't empty

    # Verify timing and cost calculations
    assert result.runTimeMs > 0
    assert result.inputAndOutputCost >= 0


def test_openai_text_prompt():
    from modules.openai_llm import text_prompt

    response = text_prompt("ping", "gpt-4o")
    assert response.response != ""
    assert response.runTimeMs > 0
    assert response.inputAndOutputCost > 0.0


def test_openai_bench_prompt():
    from modules.openai_llm import bench_prompt
    response = bench_prompt("ping", "gpt-4o")
    assert response.response != ""
    assert response.total_duration_ms > 0
    # Check that cost is computed correctly (non-negative float)
    assert isinstance(response.inputAndOutputCost, float)
    assert response.inputAndOutputCost >= 0.0


@pytest.mark.parametrize(
    "model_input,expected_reasoning",
    [
        ("o3-mini:low", "low"),
        ("o3-mini:medium", "medium"),
        ("o3-mini:high", "high"),
        ("o3-mini", None),
    ],
)
def test_text_prompt_reasoning_effort(model_input, expected_reasoning):
    """
    Test that text_prompt works with real API calls and that our parsing works.
    """
    # Double-check the parsing outcome
    from utils import parse_reasoning_effort

    base_model, effective = parse_reasoning_effort(model_input)
    assert base_model == "o3-mini", "Base model should be 'o3-mini'"
    assert (
        effective == expected_reasoning
    ), f"Expected reasoning_effort to be {expected_reasoning}"

    # Do a real API call
    from modules.openai_llm import text_prompt

    response = text_prompt("ping", model_input)

    # Validate the actual response received
    assert response.response != "", "Expected non-empty response"
    assert response.runTimeMs > 0, "Expected a positive runtime"
    assert response.inputAndOutputCost >= 0, "Expected non-negative cost"
