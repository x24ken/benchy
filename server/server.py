from flask import Flask, request, jsonify
from time import time
from modules.data_types import (
    ModelAlias,
    PromptResponse,
    PromptWithToolCalls,
    ToolCallResponse,
)
import modules.llm_models as llm_models

app = Flask(__name__)


@app.route("/prompt", methods=["POST"])
def handle_prompt():
    data = request.get_json()
    prompt = data["prompt"]
    model = ModelAlias(data["model"])

    start_time = time()
    prompt_response = llm_models.prompt(prompt, model)
    run_time_ms = int((time() - start_time) * 1000)

    # Update the runtime in the response
    prompt_response.runTimeMs = run_time_ms

    return jsonify(
        {
            "response": prompt_response.response,
            "runTimeMs": prompt_response.runTimeMs,
            "inputAndOutputCost": prompt_response.inputAndOutputCost,
        }
    )


@app.route("/tool-prompt", methods=["POST"])
def handle_tool_prompt():
    data = request.get_json()
    prompt_with_tools = PromptWithToolCalls(
        prompt=data["prompt"], model=ModelAlias(data["model"])
    )

    start_time = time()
    tool_response = llm_models.tool_prompt(prompt_with_tools)
    run_time_ms = int((time() - start_time) * 1000)

    # Update the runtime in the response
    tool_response.runTimeMs = run_time_ms

    print(f"tool_response.tool_calls: {tool_response.tool_calls}")

    return jsonify(
        {
            "tool_calls": [
                {"tool_name": tc.tool_name, "params": tc.params}
                for tc in tool_response.tool_calls
            ],
            "runTimeMs": tool_response.runTimeMs,
            "inputAndOutputCost": tool_response.inputAndOutputCost,
        }
    )


def main():
    app.run(debug=True, port=5000)


if __name__ == "__main__":
    main()
