import { reactive } from "vue";
import { ExecEvalBenchmarkModelReport } from "../types";

interface IsoSpeedBenchState {
    isLoading: boolean;
    benchmarkResults: ExecEvalBenchmarkModelReport[];
    currentIndex: number;
    intervalId: number | null;
    speed: number;
}

export const store = reactive<IsoSpeedBenchState>({
    isLoading: false,
    benchmarkResults: [],
    currentIndex: 0,
    intervalId: null,
    speed: 50
});

export function resetBenchmark() {
    store.currentIndex = 0;
    if (store.intervalId) {
        clearInterval(store.intervalId);
        store.intervalId = null;
    }
}

export function startBenchmark() {
    resetBenchmark();
    store.intervalId = setInterval(() => {
        if (store.currentIndex < store.benchmarkResults[0].results.length) {
            store.currentIndex++;
        } else {
            if (store.intervalId) {
                clearInterval(store.intervalId);
                store.intervalId = null;
            }
        }
    }, store.speed);
}
