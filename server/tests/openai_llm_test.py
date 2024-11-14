import pytest
from modules.openai_llm import tool_prompt
from modules.tools import all_tools_list
from modules.data_types import ToolCallResponse


@pytest.mark.parametrize(
    "prompt,expected_tool_calls,model",
    [
        (
            "Write code, commit it, and document it",
            ["run_coder_agent", "run_git_agent", "run_docs_agent"],
            "gpt-4o",
        ),
        ("Write some code for me", ["run_coder_agent"], "gpt-4o-mini"),
        ("Document this feature", ["run_docs_agent"], "gpt-4o"),
    ],
)
def test_tool_prompt(prompt: str, expected_tool_calls: list[str], model: str):
    result = tool_prompt(prompt=prompt, model=model, force_tools=all_tools_list)

    # Verify response type and fields
    assert isinstance(result.tools, list)
    assert isinstance(result.runTimeMs, int)
    assert isinstance(result.inputAndOutputCost, float)

    # Verify tool calls match exactly in order
    assert result.tools == expected_tool_calls

    # Verify timing and cost calculations
    assert result.runTimeMs > 0
    assert result.inputAndOutputCost >= 0
