global {
    export type RowStatus = 'idle' | 'loading' | 'success' | 'error';

    export interface RowData {
        completion: string;
        model: ModelAlias;
        correct: boolean | null;
        execution_time: number | null;
        execution_cost: number | null;
        total_cost: number;
        total_execution_time: number;
        relativePricePercent: number;
        number_correct: number;
        percent_correct: number;
        status: RowStatus;
    }

    export type ModelAlias =
        | "claude-3-5-haiku-latest"
        | "claude-3-5-sonnet-20241022"
        | "gemini-1.5-pro-002"
        | "gemini-1.5-flash-002"
        | "gemini-1.5-flash-8b-latest"
        | "gpt-4o-mini"
        | "gpt-4o"
        | "gpt-4o-predictive"
        | "gpt-4o-mini-predictive"

    export interface PromptRequest {
        prompt: string;
        model: ModelAlias;
    }

    export interface PromptResponse {
        response: string;
        runTimeMs: number;
        inputAndOutputCost: number;
    }
}


export { };
