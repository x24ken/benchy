from pydantic import BaseModel
from enum import Enum


class ModelAlias(str, Enum):
    haiku = "claude-3-5-haiku-latest"
    haiku_3_legacy = "claude-3-haiku-20240307"
    sonnet = "claude-3-5-sonnet-20241022"
    gemini_pro_2 = "gemini-1.5-pro-002"
    gemini_flash_2 = "gemini-1.5-flash-002"
    gemini_flash_8b = "gemini-1.5-flash-8b-latest"
    gpt_4o_mini = "gpt-4o-mini"
    gpt_4o = "gpt-4o"
    gpt_4o_predictive = "gpt-4o-predictive"
    gpt_4o_mini_predictive = "gpt-4o-mini-predictive"

    # JSON variants
    o1_mini_json = "o1-mini-json"
    gpt_4o_json = "gpt-4o-json"
    gpt_4o_mini_json = "gpt-4o-mini-json"
    gemini_pro_2_json = "gemini-1.5-pro-002-json"
    gemini_flash_2_json = "gemini-1.5-flash-002-json"
    sonnet_json = "claude-3-5-sonnet-20241022-json"
    haiku_json = "claude-3-5-haiku-latest-json"
    gemini_exp_1114_json = "gemini-exp-1114-json"
    llama3_2_1b = "llama3.2:1b"
    llama_3_2_3b = "llama3.2:latest"
    qwen_2_5_coder_14b = "qwen2.5-coder:14b"


class Prompt(BaseModel):
    prompt: str
    model: ModelAlias


class ToolEnum(str, Enum):
    run_coder_agent = "run_coder_agent"
    run_git_agent = "run_git_agent"
    run_docs_agent = "run_docs_agent"


class ToolAndPrompt(BaseModel):
    tool_name: ToolEnum
    prompt: str


class ToolsAndPrompts(BaseModel):
    tools_and_prompts: list[ToolAndPrompt]


class PromptWithToolCalls(BaseModel):
    prompt: str
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
