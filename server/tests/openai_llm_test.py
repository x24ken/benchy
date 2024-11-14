import pytest
from modules.openai_llm import tool_prompt
from modules.data_types import ToolCallResponse

def test_tool_prompt_all_tools():
    """Test forcing all three tools"""
    prompt = """Analyze this code, update the git repository, and update the documentation:
    
    def hello():
        print('world')
    """
    
    force_tools = ["run_coder_agent", "run_git_agent", "run_docs_agent"]
    
    result = tool_prompt(
        prompt=prompt,
        model="gpt-4o-mini",
        force_tools=force_tools
    )
    
    assert isinstance(result, ToolCallResponse)
    assert isinstance(result.tools, list)
    assert isinstance(result.runTimeMs, int)
    assert isinstance(result.inputAndOutputCost, float)
    
    # Verify all forced tools were called
    assert set(result.tools) == set(force_tools)
    assert result.runTimeMs > 0
    assert result.inputAndOutputCost >= 0

def test_tool_prompt_single_tool():
    """Test forcing just one tool"""
    prompt = "Analyze this code: print('hello')"
    force_tools = ["run_coder_agent"]
    
    result = tool_prompt(
        prompt=prompt,
        model="gpt-4o-mini",
        force_tools=force_tools
    )
    
    assert isinstance(result, ToolCallResponse)
    assert len(result.tools) == 1
    assert result.tools[0] == "run_coder_agent"
    assert result.runTimeMs > 0
    assert result.inputAndOutputCost >= 0

def test_tool_prompt_no_tools():
    """Test with empty tools list"""
    prompt = "Just say hello"
    force_tools = []
    
    result = tool_prompt(
        prompt=prompt,
        model="gpt-4o-mini", 
        force_tools=force_tools
    )
    
    assert isinstance(result, ToolCallResponse)
    assert len(result.tools) == 0
    assert result.runTimeMs > 0
    assert result.inputAndOutputCost >= 0
