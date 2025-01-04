<template>
  <div class="row">
    <div class="model-info" :class="{ 'hide-stats': modelStatDetail === 'hide' }">
      <div class="model-header">
        <img v-if="providerLogo" :src="providerLogo" :alt="provider" class="provider-logo">
        <span class="model-name">{{ modelReport.model }}</span>
      </div>
      <div v-if="modelStatDetail !== 'hide'" class="model-stats">
        <template v-if="modelStatDetail === 'verbose'">
          <div>Accuracy: {{ (modelReport.accuracy * 100).toFixed(1) }}%</div>
          <div>Tokens/sec: {{ modelReport.average_tokens_per_second.toFixed(1) }}</div>
          <div>Avg Duration: {{ modelReport.average_total_duration_ms.toFixed(0) }}ms</div>
        </template>
        <template v-else>
          <div>{{ (modelReport.accuracy * 100).toFixed(1) }}% | {{ modelReport.average_tokens_per_second.toFixed(1) }}t/s</div>
        </template>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { ExecEvalBenchmarkModelReport } from '../../types';
import anthropicLogo from '../assets/anthropic.svg';
import ollamaLogo from '../assets/ollama.svg';
import openaiLogo from '../assets/openai.svg';
import googleLogo from '../assets/google.svg';
import groqLogo from '../assets/groq.svg';

const props = defineProps<{
  modelReport: ExecEvalBenchmarkModelReport;
  scale: number;
  modelStatDetail: 'verbose' | 'simple' | 'hide';
}>();

const provider = computed(() => {
  const firstResult = props.modelReport.results[0];
  return firstResult?.prompt_response?.provider || '';
});

const providerLogo = computed(() => {
  switch (provider.value) {
    case 'anthropic':
      return anthropicLogo;
    case 'ollama':
      return ollamaLogo;
    case 'openai':
      return openaiLogo;
    case 'google':
      return googleLogo;
    case 'groq':
      return groqLogo;
    default:
      return null;
  }
});
</script>

<style scoped>
.row {
  margin-bottom: 20px;
  padding: 10px;
  border-radius: 4px;
  background-color: #f5f5f5;
}

.model-header {
  display: flex;
  align-items: center;
  gap: 8px;
}

.provider-logo {
  width: 20px;
  height: 20px;
  object-fit: contain;
}

.model-info {
  margin-bottom: 10px;
}

.model-name {
  font-weight: bold;
  font-size: 1.1em;
}

.model-stats {
  font-size: 0.9em;
  color: #666;
  margin-top: 4px;
}

.hide-stats {
  display: none;
}
</style>
