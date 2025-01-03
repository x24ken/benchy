<template>
  <div class="row">
    <div class="model-info">
      <div>{{ result.model }}</div>
      <div>{{ result.provider }}</div>
      <div>Correct: {{ result.correct_count }}</div>
      <div>Incorrect: {{ result.incorrect_count }}</div>
      <div>Accuracy: {{ (result.accuracy * 100).toFixed(2) }}%</div>
      <div>Avg TPS: {{ result.average_tokens_per_second.toFixed(2) }}</div>
      <div>Avg Duration: {{ result.average_total_duration_ms.toFixed(2) }}ms</div>
      <div>Avg Load: {{ result.average_load_duration_ms.toFixed(2) }}ms</div>
    </div>
    
    <div class="results-grid">
      <div 
        v-for="(promptResult, index) in result.results" 
        :key="index"
        :class="[
          'result-square',
          {
            'correct': promptResult.correct,
            'incorrect': !promptResult.correct,
            'pending': index >= store.currentIndex
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

defineProps<{
  modelReport: ExecEvalBenchmarkModelReport
}>();

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
