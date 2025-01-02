from flask import Flask, request, jsonify
from time import time
import yaml
from modules.data_types import (
    ModelAlias,
    PromptResponse,
    PromptWithToolCalls,
    ToolCallResponse,
    ExecEvalBenchmarkFile,
    ExecEvalBenchmarkCompleteResult,
)
import modules.llm_models as llm_models
from modules.exbench_module import run_benchmark_for_model, generate_report

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


@app.route("/iso-speed-bench", methods=["POST"])
def handle_iso_speed_bench():
    # Validate content type
    if not request.content_type == 'application/yaml':
        return jsonify({
            "error": "Invalid content type. Expected application/yaml"
        }), 415

    try:
        # Parse YAML
        try:
            yaml_data = yaml.safe_load(request.data)
            if not yaml_data:
                raise ValueError("Empty YAML file")
        except yaml.YAMLError as e:
            return jsonify({
                "error": f"Invalid YAML format: {str(e)}"
            }), 400

        # Validate structure
        try:
            benchmark_file = ExecEvalBenchmarkFile(**yaml_data)
        except ValueError as e:
            return jsonify({
                "error": f"Invalid benchmark structure: {str(e)}"
            }), 400

        # Validate models
        if not benchmark_file.models:
            return jsonify({
                "error": "No models specified in benchmark file"
            }), 400

        # Validate prompts
        if not benchmark_file.prompts:
            return jsonify({
                "error": "No prompts specified in benchmark file"
            }), 400

        # Run benchmarks
        complete_result = ExecEvalBenchmarkCompleteResult(
            benchmark_file=benchmark_file,
            results=[]
        )
        
        for model in benchmark_file.models:
            try:
                results = run_benchmark_for_model(model, benchmark_file)
                complete_result.results.extend(results)
            except Exception as e:
                return jsonify({
                    "error": f"Error running benchmark for model {model}: {str(e)}"
                }), 500

        # Generate report
        try:
            report = generate_report(complete_result)
            # Use Pydantic's model_dump() for JSON serialization
            return report.model_dump()
        except Exception as e:
            return jsonify({
                "error": f"Error generating report: {str(e)}"
            }), 500
            
    except Exception as e:
        return jsonify({
            "error": f"Unexpected error: {str(e)}"
        }), 500

def main():
    app.run(debug=True, port=5000)


if __name__ == "__main__":
    main()
