from typing import List
from modules.data_types import (
    ExecEvalBenchmarkFile,
    ExecEvalBenchmarkCompleteResult,
    ExeEvalBenchmarkOutputResult,
    ExecEvalBenchmarkModelReport,
    ExecEvalBenchmarkReport,
    ModelAlias,
)
from modules.ollama_llm import bench_prompt
from modules.execution_evaluators import execute_python_with_uv
from utils import parse_markdown_backticks


def run_benchmark_for_model(
    model: str, benchmark_file: ExecEvalBenchmarkFile
) -> List[ExeEvalBenchmarkOutputResult]:
    results = []
    for prompt_row in benchmark_file.prompts:
        # Replace dynamic variables in base prompt
        prompt = benchmark_file.base_prompt
        if prompt_row.dynamic_variables:
            for key, value in prompt_row.dynamic_variables.items():
                prompt = prompt.replace(f"{{{{{key}}}}}", str(value))

        # Get benchmark response
        bench_response = bench_prompt(prompt, model)

        # Parse and execute the response
        cleaned_code = parse_markdown_backticks(bench_response.response)
        try:
            if benchmark_file.evaluator == "execute_python_code_with_uv":
                execution_result = execute_python_with_uv(cleaned_code)
                print("execution_result", execution_result)
                correct = (
                    str(execution_result).strip() == str(prompt_row.expectation).strip()
                )
            else:
                raise ValueError(f"Unsupported evaluator: {benchmark_file.evaluator}")
        except Exception as e:
            execution_result = str(e)
            correct = False

        # Store results
        results.append(
            ExeEvalBenchmarkOutputResult(
                prompt_response=bench_response,
                model=model,  # Just use the string directly
                correct=correct,
            )
        )
    return results


def generate_report(
    complete_result: ExecEvalBenchmarkCompleteResult,
) -> ExecEvalBenchmarkReport:
    model_reports = []

    # Group results by model
    model_results = {}
    for result in complete_result.results:
        if result.model not in model_results:
            model_results[result.model] = []
        model_results[result.model].append(result)

    # Create model reports
    for model, results in model_results.items():
        correct_count = sum(1 for r in results if r.correct)
        incorrect_count = len(results) - correct_count
        accuracy = correct_count / len(results)

        avg_tokens_per_second = sum(
            r.prompt_response.tokens_per_second for r in results
        ) / len(results)
        avg_total_duration = sum(
            r.prompt_response.total_duration_ms for r in results
        ) / len(results)
        avg_load_duration = sum(
            r.prompt_response.load_duration_ms for r in results
        ) / len(results)

        model_reports.append(
            ExecEvalBenchmarkModelReport(
                model=model,
                results=results,
                correct_count=correct_count,
                incorrect_count=incorrect_count,
                accuracy=accuracy,
                average_tokens_per_second=avg_tokens_per_second,
                average_total_duration_ms=avg_total_duration,
                average_load_duration_ms=avg_load_duration,
            )
        )

    # Calculate overall statistics
    overall_correct = sum(r.correct_count for r in model_reports)
    overall_incorrect = sum(r.incorrect_count for r in model_reports)
    overall_accuracy = overall_correct / (overall_correct + overall_incorrect)

    avg_tokens_per_second = sum(
        r.average_tokens_per_second for r in model_reports
    ) / len(model_reports)
    avg_total_duration = sum(r.average_total_duration_ms for r in model_reports) / len(
        model_reports
    )
    avg_load_duration = sum(r.average_load_duration_ms for r in model_reports) / len(
        model_reports
    )

    return ExecEvalBenchmarkReport(
        benchmark_name=complete_result.benchmark_file.benchmark_name,
        purpose=complete_result.benchmark_file.purpose,
        models=model_reports,
        overall_correct_count=overall_correct,
        overall_incorrect_count=overall_incorrect,
        overall_accuracy=overall_accuracy,
        average_tokens_per_second=avg_tokens_per_second,
        average_total_duration_ms=avg_total_duration,
        average_load_duration_ms=avg_load_duration,
    ).model_dump()
