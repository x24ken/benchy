<template>
  <div class="row">
    <div
      class="model-info"
      :style="{ width: modelStatDetail === 'hide' ? 'auto' : '300px' }"
    >
      <h2>{{ modelReport.model }}</h2>
      <div
        class="model-details"
        v-if="modelStatDetail !== 'hide'"
        :class="{ 'simple-stats': modelStatDetail === 'simple' }"
      >
        <template v-if="modelStatDetail === 'verbose'">
          <div class="detail-item">
            <span class="label">Provider:</span>
            <span>{{ modelReport.results[0]?.prompt_response?.provider }}</span>
          </div>
          <div class="detail-item">
            <span class="label">Correct:</span>
            <span class="correct-count">{{ modelReport.correct_count }}</span>
          </div>
          <div class="detail-item">
            <span class="label">Incorrect:</span>
            <span class="incorrect-count">{{
              modelReport.incorrect_count
            }}</span>
          </div>
          <div class="detail-item">
            <span class="label">Accuracy:</span>
            <span>{{ (modelReport.accuracy * 100).toFixed(2) }}%</span>
          </div>
          <div class="detail-item">
            <span class="label">Avg TPS:</span>
            <span>{{ modelReport.average_tokens_per_second.toFixed(2) }}</span>
          </div>
          <div class="detail-item">
            <span class="label">Avg Duration:</span>
            <span
              >{{ modelReport.average_total_duration_ms.toFixed(2) }}ms</span
            >
          </div>
          <div class="detail-item">
            <span class="label">Avg Load:</span>
            <span>{{ modelReport.average_load_duration_ms.toFixed(2) }}ms</span>
          </div>
        </template>
        <template v-else>
          <div class="detail-item">
            <span class="label">Accuracy:</span>
            <span>{{ (modelReport.accuracy * 100).toFixed(2) }}%</span>
          </div>
          <div class="detail-item">
            <span class="label">Avg TPS:</span>
            <span>{{ modelReport.average_tokens_per_second.toFixed(2) }}</span>
          </div>
        </template>
      </div>
    </div>

    <div class="results-grid" :style="{ '--block-size': props.scale + 'px' }">
      <div
        v-for="(promptResult, index) in modelReport.results"
        :key="index"
        :class="[
          'result-square',
          {
            correct: isResultCompleted(promptResult, index) && promptResult.correct,
            incorrect: isResultCompleted(promptResult, index) && !promptResult.correct,
            pending: !isResultCompleted(promptResult, index),
            'hide-duration': scale < 100,
            'hide-tps': scale < 75,
            'hide-number': scale < 50
          },
        ]"
        @click="openModal(promptResult)"
      >
        <div class="square-content">
          <div class="index">{{ index + 1 }}</div>
          <div class="metrics" v-if="isResultCompleted(promptResult, index)">
            <div class="tps">
              {{ promptResult.prompt_response.tokens_per_second.toFixed(2) }}
              tps
            </div>
            <div class="duration">
              {{ promptResult.prompt_response.total_duration_ms.toFixed(2) }}ms
              dur
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { store } from "../stores/isoSpeedBenchStore";
import {
  ExecEvalBenchmarkModelReport,
  ExecEvalBenchmarkOutputResult,
} from "../types";

const props = defineProps<{
  modelReport: ExecEvalBenchmarkModelReport;
  scale: number;
  modelStatDetail: 'verbose' | 'simple' | 'hide';
}>();

function isResultCompleted(
  result: ExecEvalBenchmarkOutputResult,
  index: number
) {
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
  margin-bottom: v-bind('benchMode ? "20px" : "40px"');
  gap: 30px;
}

.model-info {
  min-width: 300px;
  width: 300px;
  transition: width 0.2s ease;
}

h2 {
  margin: 0 0 15px 0;
  font-size: 1.5em;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.model-details {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.detail-item {
  display: flex;
  justify-content: space-between;
}

.label {
  font-weight: 500;
  color: #666;
}

.correct-count {
  color: #4caf50;
}

.incorrect-count {
  color: #f44336;
}

.results-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
  flex: 1;
  --block-size: v-bind('scale + "px"');
}

.result-square {
  width: var(--block-size);
  height: var(--block-size);
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid #ccc;
  cursor: pointer;
  position: relative;
  transition: all 0.2s ease;
}

.hide-duration {
  .duration {
    display: none;
  }
}

.hide-tps {
  .tps {
    display: none;
  }
}

.hide-number {
  .index {
    display: none;
  }
  
  .metrics {
    display: none;
  }
  
  .square-content {
    justify-content: center;
  }
}

.square-content {
  text-align: center;
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.metrics {
  display: flex;
  flex-direction: column;
  gap: 2px;
  margin-top: 5px;
}

.duration {
  font-size: 0.8em;
  opacity: 0.8;
}

.index {
  font-size: 1.5em;
  font-weight: bold;
}

.tps {
  font-size: 0.9em;
  margin-top: 5px;
}

.pending {
  background-color: #eee;
}

.correct {
  background-color: #4caf50;
  color: white;
}

.incorrect {
  background-color: #f44336;
  color: white;
}

.simple-stats {
  .detail-item {
    &:not(:first-child):not(:nth-child(2)) {
      display: none;
    }
  }
}
</style>
