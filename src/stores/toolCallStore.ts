import { reactive } from "vue";

function loadDefaultState() {
    return {
        isLoading: false,
        promptResponses: [] as ToolCallResponse[],
        userInput: "",
        expectedToolCalls: [] as string[],
        total_executions: 0,
        activeTab: "toolcall",

        rowData: [
            {
                model: "gpt-4o-mini",
                status: 'idle',
                toolCalls: null,
                execution_time: null,
                execution_cost: null,
                total_cost: 0,
                total_execution_time: 0,
                relativePricePercent: 100,
            },
            {
                model: "gpt-4o",
                status: 'idle',
                toolCalls: null,
                execution_time: null,
                execution_cost: null,
                total_cost: 0,
                total_execution_time: 0,
                relativePricePercent: 100,
            }
        ] as ToolCallRowData[],
    };
}

function loadState() {
    const savedState = localStorage.getItem('toolCallState');
    if (savedState) {
        try {
            return JSON.parse(savedState);
        } catch (e) {
            console.error('Failed to parse saved state:', e);
            return loadDefaultState();
        }
    }
    return loadDefaultState();
}

export function resetState() {
    const defaultState = loadDefaultState();
    setState(defaultState);
    localStorage.setItem('toolCallState', JSON.stringify(store));
}

function setState(state: any) {
    store.isLoading = state.isLoading;
    store.promptResponses = state.promptResponses;
    store.userInput = state.userInput;
    store.expectedToolCalls = state.expectedToolCalls;
    store.activeTab = state.activeTab;
    store.rowData = state.rowData;
    store.total_executions = state.total_executions;
}

export const store = reactive(loadState());
