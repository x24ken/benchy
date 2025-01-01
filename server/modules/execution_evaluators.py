import subprocess


def execute_python_with_uv(code: str) -> str:
    return execute(f"uv run python -c '{code}' --ignore-warnings")


# uv run python -c 'result = ((5 + 5) / 2) * 3;print(result);' --ignore-warnings


def execute(code: str) -> str:
    """Execute the tests and return the output as a string."""
    result = subprocess.run(
        code.split(),
        capture_output=True,
        text=True,
    )
    return result.stdout + result.stderr
