import llm
from dotenv import load_dotenv
import os
from modules.data_types import (
    ModelAlias,
    PromptResponse,
    PromptWithToolCalls,
    ToolCallResponse,
)
from modules import openai_llm, gemini_llm
from utils import MAP_MODEL_ALIAS_TO_COST_PER_MILLION_TOKENS
from modules.tools import all_tools_list
from modules import anthropic_llm

# Load environment variables from .env file
load_dotenv()


def parse_input_and_output_tokens_from_completion(
    llm_prompt_completion: dict,
    model_alias: ModelAlias,
) -> tuple[int, int]:
    if model_alias in [ModelAlias.gpt_4o, ModelAlias.gpt_4o_mini]:
        # OpenAI format
        usage = llm_prompt_completion.get("usage", {})
        return usage.get("prompt_tokens", 0), usage.get("completion_tokens", 0)

    elif model_alias in [
        ModelAlias.gemini_pro_2,
        ModelAlias.gemini_flash_2,
        ModelAlias.gemini_flash_8b,
    ]:
        # Gemini format - get from last item in list which has full token counts
        usage = llm_prompt_completion[-1].get("usageMetadata", {})
        return usage.get("promptTokenCount", 0), usage.get("candidatesTokenCount", 0)

    elif model_alias in [ModelAlias.sonnet, ModelAlias.haiku]:
        # Claude format
        usage = llm_prompt_completion.get("usage", {})
        return usage.get("input_tokens", 0), usage.get("output_tokens", 0)

    return 0, 0


def get_cost(model: ModelAlias, input_tokens: int, output_tokens: int) -> float:
    """
    Calculate the cost of a model run based on input and output tokens.

    Args:
        model: The ModelAlias used
        input_tokens: Number of input tokens used
        output_tokens: Number of output tokens used

    Returns:
        float: Total cost in dollars
    """
    cost_map = MAP_MODEL_ALIAS_TO_COST_PER_MILLION_TOKENS.get(model)
    if not cost_map:
        return 0.0

    input_cost = (input_tokens / 1_000_000) * cost_map["input"]
    output_cost = (output_tokens / 1_000_000) * cost_map["output"]

    return round(input_cost + output_cost, 6)


def build_model_map() -> dict[ModelAlias, llm.Model]:
    model_map = {}

    # Build GPT-4 models
    gpt4_o_latest: llm.Model = llm.get_model("gpt-4o")
    gpt4_o_mini: llm.Model = llm.get_model("gpt-4o-mini")
    model_map[ModelAlias.gpt_4o] = gpt4_o_latest
    model_map[ModelAlias.gpt_4o_mini] = gpt4_o_mini

    # Build Gemini models
    gemini_1_5_pro_002: llm.Model = llm.get_model("gemini-1.5-pro-002")
    gemini_1_5_flash_002: llm.Model = llm.get_model("gemini-1.5-flash-002")
    gemini_1_5_flash_8b: llm.Model = llm.get_model("gemini-1.5-flash-8b-latest")
    model_map[ModelAlias.gemini_pro_2] = gemini_1_5_pro_002
    model_map[ModelAlias.gemini_flash_2] = gemini_1_5_flash_002
    model_map[ModelAlias.gemini_flash_8b] = gemini_1_5_flash_8b

    # Build Anthropic model
    sonnet_model = llm.get_model("claude-3-5-sonnet-latest")
    haiku_model = llm.get_model("claude-3-5-haiku-latest")
    model_map[ModelAlias.sonnet] = sonnet_model
    model_map[ModelAlias.haiku] = haiku_model

    return model_map


def llm_prompt(
    prompt: str, model_alias: ModelAlias, model: llm.Model
) -> PromptResponse:
    res = model.prompt(prompt, stream=False)
    completion_json = res.json()

    # Extract response text based on model type
    if model_alias in [ModelAlias.gpt_4o, ModelAlias.gpt_4o_mini]:
        response_text = res.text()
    elif model_alias in [
        ModelAlias.gemini_pro_2,
        ModelAlias.gemini_flash_2,
        ModelAlias.gemini_flash_8b,
    ]:
        response_text = res.text()
    elif model_alias in [ModelAlias.sonnet, ModelAlias.haiku]:
        response_text = res.text()
    else:
        response_text = ""

    # Get token counts and calculate cost
    input_tokens, output_tokens = parse_input_and_output_tokens_from_completion(
        completion_json, model_alias
    )
    cost = get_cost(model_alias, input_tokens, output_tokens)

    return PromptResponse(response=response_text, runTimeMs=0, inputAndOutputCost=cost)


def prompt(prompt: str, model_alias: ModelAlias) -> PromptResponse:
    model: llm.Model = model_map.get(model_alias)

    if model_alias == ModelAlias.gpt_4o_predictive:
        return openai_llm.predictive_prompt(prompt, prompt, "gpt-4o")
    elif model_alias == ModelAlias.gpt_4o_mini_predictive:
        return openai_llm.predictive_prompt(prompt, prompt, "gpt-4o-mini")
    elif model is not None:
        return llm_prompt(prompt, model_alias, model)
    else:
        raise ValueError(f"Model {model_alias} not found")


def tool_prompt(prompt: PromptWithToolCalls) -> ToolCallResponse:
    model: llm.Model = model_map.get(prompt.model)
    if model is None:
        raise ValueError(f"Model {prompt.model} not found")

    if prompt.model in [ModelAlias.gpt_4o, ModelAlias.gpt_4o_mini]:
        return openai_llm.tool_prompt(prompt.prompt, prompt.model, all_tools_list)
    elif prompt.model == ModelAlias.sonnet:
        return anthropic_llm.tool_prompt(prompt.prompt)
    elif prompt.model in [ModelAlias.gemini_pro_2, ModelAlias.gemini_flash_2]:
        return gemini_llm.tool_prompt(prompt.prompt, prompt.model, all_tools_list)

    raise ValueError(f"Model {prompt.model} not supported for tool calls")


model_map: dict[ModelAlias, llm.Model] = build_model_map()
