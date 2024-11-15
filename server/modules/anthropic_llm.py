import anthropic
import os
import json
from modules.data_types import ModelAlias
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
    # Map the model string to ModelAlias
    model_alias = (
        ModelAlias.sonnet 
        if "claude-3-5-sonnet" in model 
        else ModelAlias.haiku 
        if "claude-3-5-haiku" in model
        else None
    )
    
    if not model_alias:
        return 0.0

    cost_map = MAP_MODEL_ALIAS_TO_COST_PER_MILLION_TOKENS.get(model_alias)
    if not cost_map:
        return 0.0

    input_cost = (input_tokens / 1_000_000) * cost_map["input"]
    output_cost = (output_tokens / 1_000_000) * cost_map["output"]

    return round(input_cost + output_cost, 6)


def tool_prompt(prompt: str, model: str = "claude-3-5-sonnet-20241022") -> ToolCallResponse:
    """
    Run a chat model with tool calls using Anthropic's Claude.

    Args:
        prompt (str): The prompt to send to the Anthropic API.
        model (str): The model ID to use (defaults to Claude 3 Sonnet)

    Returns:
        ToolCallResponse: The response including tools called, runtime, and cost.
    """

    with timeit() as t:
        message = anthropic_client.messages.create(
            model=model,
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}],
            tools=anthropic_tools_list,
            tool_choice={"type": "any"},
        )

    # Extract tool calls with parameters and execute them
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
