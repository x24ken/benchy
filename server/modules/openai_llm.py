import openai
import os
import json
from modules.tools import openai_tools_list
from modules.data_types import SimpleToolCall
from utils import timeit
from modules.data_types import PromptResponse, ModelAlias, ToolCallResponse
from utils import MAP_MODEL_ALIAS_TO_COST_PER_MILLION_TOKENS
from modules.tools import all_tools_list

openai_client: openai.OpenAI = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def get_openai_cost(model: str, input_tokens: int, output_tokens: int) -> float:
    """
    Calculate the cost for OpenAI API usage.

    Args:
        model: The model name/alias used
        input_tokens: Number of input tokens
        output_tokens: Number of output tokens

    Returns:
        float: Total cost in dollars
    """
    # Map the OpenAI model name to our ModelAlias
    model_alias = ModelAlias.gpt_4o if "gpt-4" in model else ModelAlias.gpt_4o_mini

    cost_map = MAP_MODEL_ALIAS_TO_COST_PER_MILLION_TOKENS.get(model_alias)
    if not cost_map:
        return 0.0

    input_cost = (input_tokens / 1_000_000) * cost_map["input"]
    output_cost = (output_tokens / 1_000_000) * cost_map["output"]

    return round(input_cost + output_cost, 6)


def tool_prompt(prompt: str, model: str, force_tools: list[str]) -> ToolCallResponse:
    """
    Run a chat model forcing specific tool calls.

    Args:
        prompt (str): The prompt to send to the OpenAI API.
        model (str): The model ID to use for the API call.
        force_tools (list[str]): List of tool names to force call.

    Returns:
        ToolCallResponse: The response including tools called, runtime, and cost.
    """
    # Filter tools to only include forced ones

    with timeit() as t:
        completion = openai_client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            tools=openai_tools_list,
            tool_choice="required",
        )

    # Extract token counts and calculate cost
    input_tokens = completion.usage.prompt_tokens
    output_tokens = completion.usage.completion_tokens
    cost = get_openai_cost(model, input_tokens, output_tokens)

    # Extract tool calls with parameters
    tool_calls = []
    if completion.choices[0].message.tool_calls:
        tool_calls = [
            SimpleToolCall(
                tool_name=tool_call.function.name,
                params=json.loads(tool_call.function.arguments),
            )
            for tool_call in completion.choices[0].message.tool_calls
        ]

    return ToolCallResponse(
        tool_calls=tool_calls, runTimeMs=t(), inputAndOutputCost=cost
    )


def predictive_prompt(prompt: str, prediction: str, model: str) -> PromptResponse:
    """
    Run a chat model with a predicted output to reduce latency.

    Args:
        prompt (str): The prompt to send to the OpenAI API.
        prediction (str): The predicted output text.
        model (str): The model ID to use for the API call.

    Returns:
        PromptResponse: The response including text, runtime, and cost.
    """
    # Prepare the API call parameters outside the timing block
    messages = [{"role": "user", "content": prompt}]
    prediction_param = {"type": "content", "content": prediction}

    # Only time the actual API call
    with timeit() as t:
        completion = openai_client.chat.completions.create(
            model=model,
            messages=messages,
            prediction=prediction_param,
        )

    # Process results after timing block
    input_tokens = completion.usage.prompt_tokens
    output_tokens = completion.usage.completion_tokens
    cost = get_openai_cost(model, input_tokens, output_tokens)

    return PromptResponse(
        response=completion.choices[0].message.content,
        runTimeMs=t(),  # Get the elapsed time of just the API call
        inputAndOutputCost=cost,
    )
