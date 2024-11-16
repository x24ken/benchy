import anthropic
import os
import json
from modules.data_types import ModelAlias, ToolsAndPrompts
from utils import MAP_MODEL_ALIAS_TO_COST_PER_MILLION_TOKENS
from modules.data_types import SimpleToolCall, ToolCallResponse
from utils import timeit
from modules.tools import (
    anthropic_tools_list,
    run_coder_agent,
    run_git_agent,
    run_docs_agent,
    all_tools_list,
)

# Initialize Anthropic client
anthropic_client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


def get_anthropic_cost(model: str, input_tokens: int, output_tokens: int) -> float:
    """
    Calculate the cost for Anthropic API usage.

    Args:
        model: The model name/alias used
        input_tokens: Number of input tokens
        output_tokens: Number of output tokens

    Returns:
        float: Total cost in dollars
    """

    cost_map = MAP_MODEL_ALIAS_TO_COST_PER_MILLION_TOKENS.get(model)
    if not cost_map:
        return 0.0

    input_cost = (input_tokens / 1_000_000) * cost_map["input"]
    output_cost = (output_tokens / 1_000_000) * cost_map["output"]

    return round(input_cost + output_cost, 6)


def tool_prompt(prompt: str, model: str) -> ToolCallResponse:
    """
    Run a chat model with tool calls using Anthropic's Claude.
    Now supports JSON structured output variants by parsing the response.
    """
    with timeit() as t:
        if "-json" in model:
            # Standard message request but expecting JSON response
            message = anthropic_client.messages.create(
                model=model.replace("-json", ""),
                max_tokens=2048,
                messages=[{"role": "user", "content": prompt}],
            )

            try:
                # Parse raw response text into ToolsAndPrompts model
                parsed_response = ToolsAndPrompts.model_validate_json(
                    message.content[0].text
                )
                tool_calls = [
                    SimpleToolCall(
                        tool_name=tap.tool_name, params={"prompt": tap.prompt}
                    )
                    for tap in parsed_response.tools_and_prompts
                ]
            except Exception as e:
                print(f"Failed to parse JSON response: {e}")
                tool_calls = []

        else:
            # Original implementation for function calling
            message = anthropic_client.messages.create(
                model=model,
                max_tokens=2048,
                messages=[{"role": "user", "content": prompt}],
                tools=anthropic_tools_list,
                tool_choice={"type": "any"},
            )

            # Extract tool calls with parameters
            tool_calls = []
            for content in message.content:
                if content.type == "tool_use":
                    tool_name = content.name
                    if tool_name in all_tools_list:
                        tool_calls.append(
                            SimpleToolCall(tool_name=tool_name, params=content.input)
                        )

    # Calculate cost based on token usage
    input_tokens = message.usage.input_tokens
    output_tokens = message.usage.output_tokens
    cost = get_anthropic_cost(model, input_tokens, output_tokens)

    return ToolCallResponse(
        tool_calls=tool_calls, runTimeMs=t(), inputAndOutputCost=cost
    )
