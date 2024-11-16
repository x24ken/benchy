import google.generativeai as genai
import os
import json
from modules.tools import gemini_tools_list
from modules.data_types import SimpleToolCall, ModelAlias
from utils import timeit, MAP_MODEL_ALIAS_TO_COST_PER_MILLION_TOKENS
from modules.data_types import ToolCallResponse

# Initialize Gemini client
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


def get_gemini_cost(model: str, input_tokens: int, output_tokens: int) -> float:
    """
    Calculate the cost for Gemini API usage.

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


def tool_prompt(prompt: str, model: str, force_tools: list[str]) -> ToolCallResponse:
    """
    Run a chat model with tool calls using Gemini's API.

    This implementation uses Gemini's native function calling capabilities to:
    1. Process the user's prompt
    2. Select and call appropriate tools
    3. Return structured tool call responses

    Args:
        prompt (str): The prompt to send to the Gemini API
        model (str): The model ID to use (e.g. "gemini-1.5-pro-002")
        force_tools (list[str]): List of tool names to force call

    Returns:
        ToolCallResponse: The response including tools called, runtime, and cost
    """
    # Initialize the model
    gemini_model = genai.GenerativeModel(model_name=model, tools=gemini_tools_list)

    with timeit() as t:
        # Start a chat that automatically handles function calling
        chat = gemini_model.start_chat(enable_automatic_function_calling=True)

        # Send the message and get the response
        response = chat.send_message(prompt)

        # Extract tool calls from the response parts
        tool_calls = []
        for part in response.parts:
            if hasattr(part, "function_call"):
                fc = part.function_call
                tool_calls.append(SimpleToolCall(tool_name=fc.name, params=fc.args))

        # Extract token counts from usage metadata
        usage_metadata = response._result.usage_metadata
        input_tokens = usage_metadata.prompt_token_count
        output_tokens = usage_metadata.candidates_token_count

        # Calculate cost based on token usage
        cost = get_gemini_cost(model, input_tokens, output_tokens)

    return ToolCallResponse(
        tool_calls=tool_calls, runTimeMs=t(), inputAndOutputCost=cost
    )
