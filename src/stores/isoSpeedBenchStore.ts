import { reactive } from "vue";
import { ExecEvalBenchmarkReport } from "../types";

interface IsoSpeedBenchState {
    isLoading: boolean;
    benchmarkReport: ExecEvalBenchmarkReport | null;
    currentTime: number;
    intervalId: number | null;
    speed: number;
    isReplaying: boolean;
    completedResults: Set<string>;
}

export const store = reactive<IsoSpeedBenchState>({
    isLoading: false,
    benchmarkReport: null,
    currentTime: 0,
    intervalId: null,
    speed: 50,
    isReplaying: false,
    completedResults: new Set()
});

export function resetBenchmark() {
    store.currentTime = 0;
    store.completedResults.clear();
    store.isReplaying = false;
    if (store.intervalId) {
        clearInterval(store.intervalId);
        store.intervalId = null;
    }
}

export function startBenchmark() {
    resetBenchmark();
    store.isReplaying = true;

    store.intervalId = setInterval(() => {
        store.currentTime += store.speed;

        store.benchmarkReport?.models.forEach(modelReport => {
            // Calculate cumulative time for each result
            let cumulativeTime = 0;

            modelReport.results.forEach((result, index) => {
                cumulativeTime += result.prompt_response.total_duration_ms;
                const resultKey = `${modelReport.model}-${index}`;

                if (!store.completedResults.has(resultKey) &&
                    store.currentTime >= cumulativeTime) {
                    store.completedResults.add(resultKey);
                }
            });
        });

        // Check if all results are completed
        const totalResults = store.benchmarkReport?.models.reduce((acc, model) =>
            acc + model.results.length, 0) || 0;

        if (store.completedResults.size >= totalResults) {
            if (store.intervalId) {
                clearInterval(store.intervalId);
                store.intervalId = null;
                store.isReplaying = false;
            }
        }
    }, store.speed);
}

export const inMemoryBenchmarkReport: ExecEvalBenchmarkReport = {
    "benchmark_name": "Simple Math in Python",
    "purpose": "Evaluate the ability of a language model to perform simple mathematical operations in Python.",
    "models": [
        {
            "model": "llama3.2:1b",
            "results": [
                {
                    "prompt_response": {
                        "response": "Here's a simple Python script that accomplishes this:\n\n```python\nprint(5 + 5)\n```\n\nWhen you run this script, it will output `10`, which is the result of adding 5 and 5. \n\nThis code is a direct example of a mathematical statement in Python, where we specify two operands (in this case, 5 and 5) and an operator (+). The operator determines the type of operation to perform on the operands. In this case, it's a simple addition.",
                        "tokens_per_second": 169.32907348242813,
                        "provider": "ollama",
                        "total_duration_ms": 1285.184375,
                        "load_duration_ms": 556.818292,
                        "errored": null
                    },
                    "execution_result": "10.0",
                    "expected_result": "10",
                    "input_prompt": "Exclusively output python code: Create and print the mathematical statement for the following: add 5 and 5\n",
                    "model": "llama3.2:1b",
                    "correct": true,
                    "index": 1
                },
                {
                    "prompt_response": {
                        "response": "```python\nresult = (5 + 5) / 2 * 3\nprint(result)\n```\n\nAlternatively, you can use a more Pythonic approach using list comprehension:\n\n```python\nresult = [5, 5].append(0)[1:] * 3\nprint(result)\n```",
                        "tokens_per_second": 166.66666666666666,
                        "provider": "ollama",
                        "total_duration_ms": 411.833667,
                        "load_duration_ms": 15.9625,
                        "errored": null
                    },
                    "execution_result": "Error:   File \"/var/folders/5x/kqd2skpd1z1d0b_htgj3bhd00000gn/T/tmp778ad0zt.py\", line 3\n    ```\n    ^\nSyntaxError: invalid syntax\n",
                    "expected_result": "15",
                    "input_prompt": "Exclusively output python code: Create and print the mathematical statement for the following: add 5 and 5 then split in half then triple\n",
                    "model": "llama3.2:1b",
                    "correct": false,
                    "index": 2
                },
                {
                    "prompt_response": {
                        "response": "```python\n# Mathematical statement: Multiply 3 by 4 and add 7\nstatement = \"3 * 4 + 7\"\nprint(statement)\n```\n\nYou can also use string formatting to achieve the same result:\n\n```python\n# Mathematical statement: Multiply 3 by 4 and add 7\nnum1, num2, operator, num3 = 3, 4, \"+\", 7\nstatement = \"{} {} {} {}\".format(num1, operator, num2, num3)\nprint(statement)\n```\n\nOr using f-strings (Python 3.6+):\n\n```python\n# Mathematical statement: Multiply 3 by 4 and add 7\nnum1, num2, operator, num3 = 3, 4, \"+\", 7\nstatement = f\"{num1} {operator} {num2} {num3}\"\nprint(statement)\n```",
                        "tokens_per_second": 163.28331862312444,
                        "provider": "ollama",
                        "total_duration_ms": 1164.869625,
                        "load_duration_ms": 13.80175,
                        "errored": null
                    },
                    "execution_result": "Error:   File \"/var/folders/5x/kqd2skpd1z1d0b_htgj3bhd00000gn/T/tmp5zdl0xwx.py\", line 4\n    ```\n    ^\nSyntaxError: invalid syntax\n",
                    "expected_result": "19",
                    "input_prompt": "Exclusively output python code: Create and print the mathematical statement for the following: multiply 3 by 4 and add 7\n",
                    "model": "llama3.2:1b",
                    "correct": false,
                    "index": 3
                }
            ],
            "correct_count": 1,
            "incorrect_count": 2,
            "accuracy": 0.3333333333333333,
            "average_tokens_per_second": 166.4263529240731,
            "average_total_duration_ms": 953.9625556666666,
            "average_load_duration_ms": 195.527514
        },
        {
            "model": "qwen2.5-coder:14b",
            "results": [
                {
                    "prompt_response": {
                        "response": "```python\nresult = 5 + 5\nprint(\"The result of adding 5 and 5 is:\", result)\n```",
                        "tokens_per_second": 31.890660592255124,
                        "provider": "ollama",
                        "total_duration_ms": 2116.46125,
                        "load_duration_ms": 543.371,
                        "errored": null
                    },
                    "execution_result": "The result of adding 5 and 5 is: 10\n",
                    "expected_result": "10",
                    "input_prompt": "Exclusively output python code: Create and print the mathematical statement for the following: add 5 and 5\n",
                    "model": "qwen2.5-coder:14b",
                    "correct": false,
                    "index": 1
                },
                {
                    "prompt_response": {
                        "response": "```python\n# Step-by-step calculation\naddition_result = 5 + 5\nsplit_in_half = addition_result / 2\ntriple_result = split_in_half * 3\n\n# Print the final result\nprint(\"The result of adding 5 and 5, then splitting in half, and finally tripling is:\", triple_result)\n```",
                        "tokens_per_second": 30.910609857978276,
                        "provider": "ollama",
                        "total_duration_ms": 2583.297541,
                        "load_duration_ms": 14.031958,
                        "errored": null
                    },
                    "execution_result": "The result of adding 5 and 5, then splitting in half, and finally tripling is: 15.0\n",
                    "expected_result": "15",
                    "input_prompt": "Exclusively output python code: Create and print the mathematical statement for the following: add 5 and 5 then split in half then triple\n",
                    "model": "qwen2.5-coder:14b",
                    "correct": false,
                    "index": 2
                },
                {
                    "prompt_response": {
                        "response": "```python\nresult = 3 * 4 + 7\nprint(result)\n```",
                        "tokens_per_second": 32.25806451612903,
                        "provider": "ollama",
                        "total_duration_ms": 776.636334,
                        "load_duration_ms": 12.421917,
                        "errored": null
                    },
                    "execution_result": "19.0",
                    "expected_result": "19",
                    "input_prompt": "Exclusively output python code: Create and print the mathematical statement for the following: multiply 3 by 4 and add 7\n",
                    "model": "qwen2.5-coder:14b",
                    "correct": true,
                    "index": 3
                }
            ],
            "correct_count": 1,
            "incorrect_count": 2,
            "accuracy": 0.3333333333333333,
            "average_tokens_per_second": 31.686444988787475,
            "average_total_duration_ms": 1825.4650416666666,
            "average_load_duration_ms": 189.94162500000002
        }
    ],
    "overall_correct_count": 2,
    "overall_incorrect_count": 4,
    "overall_accuracy": 0.3333333333333333,
    "average_tokens_per_second": 99.05639895643029,
    "average_total_duration_ms": 1389.7137986666667,
    "average_load_duration_ms": 192.73456950000002
}
