import subprocess


def execute_python_with_uv(code: str) -> str:
    # Remove any surrounding quotes and whitespace
    code = code.strip().strip("'").strip('"')
    
    # Create a temporary file with the code
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=True) as tmp:
        tmp.write(code)
        tmp.flush()
        
        # Execute the temporary file using uv
        return execute(f"uv run {tmp.name} --ignore-warnings")


def execute(code: str) -> str:
    """Execute the tests and return the output as a string."""
    try:
        result = subprocess.run(
            code.split(),
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            return f"Error: {result.stderr}"
        return result.stdout
    except Exception as e:
        return f"Execution error: {str(e)}"
