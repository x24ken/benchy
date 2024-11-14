import time
from contextlib import contextmanager
from typing import Generator
from modules.data_types import ModelAlias

@contextmanager
def timeit() -> Generator[None, None, float]:
    """
    Context manager to measure execution time in milliseconds.
    
    Usage:
        with timeit() as t:
            # code to time
        elapsed_ms = t()
    
    Returns:
        Generator that yields None and returns elapsed time in milliseconds
    """
    start = time.perf_counter()
    yield lambda: int((time.perf_counter() - start) * 1000)

MAP_MODEL_ALIAS_TO_COST_PER_MILLION_TOKENS = {
    ModelAlias.gpt_4o_mini: {
        "input": 0.15,
        "output": 0.60,
    },
    ModelAlias.gpt_4o: {
        "input": 2.50,
        "output": 10.00,
    },
    ModelAlias.gpt_4o_predictive: {
        "input": 2.50,
        "output": 10.00,
    },
    ModelAlias.gpt_4o_mini_predictive: {
        "input": 0.15,
        "output": 0.60,
    },
    ModelAlias.haiku: {
        "input": 1.00,
        "output": 5.00,
    },
    ModelAlias.sonnet: {
        "input": 3.00,
        "output": 15.00,
    },
    ModelAlias.gemini_pro_2: {
        "input": 1.25,
        "output": 5.00,
    },
    ModelAlias.gemini_flash_2: {
        "input": 0.075,
        "output": 0.300,
    },
    ModelAlias.gemini_flash_8b: {
        "input": 0.0375,
        "output": 0.15,
    },
}
