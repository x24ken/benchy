import typer
from typing import List
import yaml
from pathlib import Path
from datetime import datetime
import json
from modules.data_types import (
    ExecEvalBenchmarkFile,
    ExecEvalBenchmarkCompleteResult,
    ModelAlias,
)
from modules.exbench_module import run_benchmark_for_model, generate_report

app = typer.Typer()


@app.command()
def ping():
    typer.echo("pong")


@app.command()
def ollama_bench(
    models: List[str] = typer.Argument(..., help="List of models to benchmark"),
    yaml_file: str = typer.Argument(
        ..., help="Path to YAML benchmark configuration file"
    ),
    output_dir: str = typer.Option(
        "reports",
        "--output-dir",
        "-o",
        help="Directory to save benchmark reports",
        exists=True,
        file_okay=False,
        dir_okay=True,
        writable=True,
        resolve_path=True,
    ),
    count: int = typer.Option(
        None,
        "--count",
        "-c",
        help="Limit the number of tests to run from the YAML file",
        min=1,
    ),
):
    """
    Run benchmarks on Ollama models using a YAML configuration file.

    Example usage:

    uv run python exbench.py ollama-bench llama3.2:1b llama3.2:latest benchmark_data/simple_math.yaml -c 5

    uv run python exbench.py ollama-bench vanilj/Phi-4:latest benchmark_data/simple_math.yaml -c 5
    """
    # Validate models
    model_aliases = []
    for model in models:
        try:
            model_aliases.append(ModelAlias[model])
        except KeyError:
            typer.echo(f"No model alias for {model}, using raw model name")
            model_aliases.append(model)

    # Load and validate YAML file
    try:
        with open(yaml_file) as f:
            yaml_data = yaml.safe_load(f)
        benchmark_file = ExecEvalBenchmarkFile(**yaml_data)
    except Exception as e:
        typer.echo(f"Error loading YAML file: {e}")
        raise typer.Exit(code=1)

    # Limit number of prompts if count is specified
    if count is not None:
        benchmark_file.prompts = benchmark_file.prompts[:count]
        typer.echo(f"Limiting to first {count} tests")

    # Create output directory if it doesn't exist
    Path(output_dir).mkdir(exist_ok=True)

    # Run benchmarks
    complete_result = ExecEvalBenchmarkCompleteResult(
        benchmark_file=benchmark_file, results=[]
    )

    for model in model_aliases:
        typer.echo(f"Running benchmarks for model: {model.value}")
        model_results = run_benchmark_for_model(model, benchmark_file)
        complete_result.results.extend(model_results)

    # Generate and save report
    report = generate_report(complete_result)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_filename = f"{output_dir}/{benchmark_file.benchmark_name}_{timestamp}.json"

    with open(report_filename, "w") as f:
        json.dump(report.dict(), f, indent=2)

    typer.echo(f"Benchmark report saved to: {report_filename}")


if __name__ == "__main__":
    app()
