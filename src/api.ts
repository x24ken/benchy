import { calculatePercentCorrect, store } from "./store";

async function sendPrompt(prompt: string, model: ModelAlias): Promise<PromptResponse> {
    const response = await fetch('/prompt', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            prompt,
            model,
        }),
    });

    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }

    return await response.json();
}

export async function runAutocomplete() {
    if (store.isLoading) return;

    console.log("Running autocomplete");

    store.isLoading = true;
    store.promptResponses = [];
    store.total_executions += 1;

    // Process each model independently
    store.rowData.forEach(async (row: RowData) => {
        const rowIndex = store.rowData.findIndex((r: RowData) => r.model === row.model);
        if (rowIndex === -1) return;

        // Set status to loading
        store.rowData[rowIndex].status = 'loading';
        store.rowData[rowIndex].completion = '';
        store.rowData[rowIndex].execution_time = 0;

        try {
            console.log(`Running autocomplete for '${row.model}'`);
            const completedPrompt = store.basePrompt.replace(
                "{input_text}",
                store.userInput
            );

            const response = await sendPrompt(completedPrompt, row.model);

            // Update row with results
            const updatedRow = { ...store.rowData[rowIndex] };
            updatedRow.completion = response.response;
            updatedRow.execution_time = response.runTimeMs;
            updatedRow.execution_cost = response.inputAndOutputCost;
            updatedRow.total_cost = Number(((updatedRow.total_cost || 0) + response.inputAndOutputCost).toFixed(6));
            updatedRow.total_execution_time = (updatedRow.total_execution_time || 0) + response.runTimeMs;
            updatedRow.number_correct = Math.min(updatedRow.number_correct + 1, store.total_executions);
            updatedRow.percent_correct = calculatePercentCorrect(updatedRow.number_correct);
            updatedRow.status = 'success';
            store.promptResponses.push(response);

            console.log(`Success: '${row.model}': '${response.response}'`);
            store.rowData.splice(rowIndex, 1, updatedRow);

            // After all rows complete, calculate relative percentages
            const allComplete = store.rowData.every(row => 
                row.status === 'success' || row.status === 'error'
            );
            
            if (allComplete) {
                const lowestCost = Math.min(...store.rowData
                    .filter(row => row.total_cost > 0)
                    .map(row => row.total_cost));
                
                store.rowData.forEach((row, idx) => {
                    const updatedRow = { ...row };
                    updatedRow.relativePricePercent = row.total_cost > 0 
                        ? Math.round((row.total_cost / lowestCost) * 100)
                        : 0;
                    store.rowData.splice(idx, 1, updatedRow);
                });
            }
        } catch (error) {
            console.error(`Error processing model '${row.model}':`, error);
            const updatedRow = { ...store.rowData[rowIndex] };
            updatedRow.completion = "Error occurred";
            updatedRow.execution_time = 0;
            updatedRow.number_correct = Math.max(0, updatedRow.number_correct - 1);
            updatedRow.percent_correct = calculatePercentCorrect(updatedRow.number_correct);
            updatedRow.status = 'error';
            store.rowData.splice(rowIndex, 1, updatedRow);
        }
    });

    store.isLoading = false;
}
