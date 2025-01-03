<template>
  <div class="row">
    <div class="model-info">
      <div>{{ modelReport.model }}</div>
      <div>{{ modelReport.results[0]?.prompt_response?.provider }}</div>
      <div>Correct: {{ modelReport.correct_count }}</div>
      <div>Incorrect: {{ modelReport.incorrect_count }}</div>
      <div>Accuracy: {{ (modelReport.accuracy * 100).toFixed(2) }}%</div>
      <div>Avg TPS: {{ modelReport.average_tokens_per_second.toFixed(2) }}</div>
      <div>Avg Duration: {{ modelReport.average_total_duration_ms.toFixed(2) }}ms</div>
      <div>Avg Load: {{ modelReport.average_load_duration_ms.toFixed(2) }}ms</div>
    </div>
    
    <div class="results-grid">
      <div 
        v-for="(promptResult, index) in modelReport.results" 
        :key="index"
        :class="[
          'result-square',
          {
            'correct': isResultCompleted(promptResult, index) && promptResult.correct,
            'incorrect': isResultCompleted(promptResult, index) && !promptResult.correct,
            'pending': !isResultCompleted(promptResult, index)
          }
        ]"
        @click="openModal(promptResult)"
      >
        {{ index + 1 }}
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { store } from "../stores/isoSpeedBenchStore";
import { ExecEvalBenchmarkModelReport, ExecEvalBenchmarkOutputResult } from "../types";

const props = defineProps<{
  modelReport: ExecEvalBenchmarkModelReport
}>();

function isResultCompleted(result: ExecEvalBenchmarkOutputResult, index: number) {
  // Calculate cumulative time up to this result
  const cumulativeTime = props.modelReport.results
    .slice(0, index + 1)
    .reduce((sum, r) => sum + r.prompt_response.total_duration_ms, 0);
    
  return store.currentTime >= cumulativeTime;
}

function openModal(result: ExecEvalBenchmarkOutputResult) {
  // Implement modal opening logic
}
</script>

<style scoped>
.row {
  display: flex;
  margin-bottom: 20px;
}

.model-info {
  width: 300px;
  padding-right: 20px;
}

.results-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
}

.result-square {
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid #ccc;
  cursor: pointer;
}

.pending {
  background-color: #eee;
}

.correct {
  background-color: #4caf50;
}

.incorrect {
  background-color: #f44336;
}
</style>
