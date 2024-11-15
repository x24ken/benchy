from pydantic import BaseModel
from enum import Enum


class ModelAlias(str, Enum):
    haiku = "claude-3-5-haiku-latest"
    sonnet = "claude-3-5-sonnet-20241022"
    gemini_pro_2 = "gemini-1.5-pro-002"
    gemini_flash_2 = "gemini-1.5-flash-002"
    gemini_flash_8b = "gemini-1.5-flash-8b-latest"
    gpt_4o_mini = "gpt-4o-mini"
    gpt_4o = "gpt-4o"

    gpt_4o_predictive = "gpt-4o-predictive"
    gpt_4o_mini_predictive = "gpt-4o-mini-predictive"


class Prompt(BaseModel):
    prompt: str
    model: ModelAlias


class PromptWithToolCalls(BaseModel):
    prompt: str
    expected_tool_calls: list[str]
    model: ModelAlias


class PromptResponse(BaseModel):
    response: str
    runTimeMs: int
    inputAndOutputCost: float


class SimpleToolCall(BaseModel):
    tool_name: str
    params: dict


class ToolCallResponse(BaseModel):
    tool_calls: list[SimpleToolCall]
    runTimeMs: int
    inputAndOutputCost: float
