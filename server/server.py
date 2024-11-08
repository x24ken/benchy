from flask import Flask, request, jsonify
from time import time
from data_types import ModelAlias, PromptResponse
import llm_models

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

    return jsonify({
        "response": prompt_response.response,
        "runTimeMs": prompt_response.runTimeMs,
        "inputAndOutputCost": prompt_response.inputAndOutputCost
    })


def main():
    app.run(debug=True, port=5000)


if __name__ == "__main__":
    main()
