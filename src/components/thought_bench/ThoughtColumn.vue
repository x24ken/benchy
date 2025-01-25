<template>
  <div 
    class="thought-column" 
    :class="columnData.state"
    :style="{ width: `${store.settings.columnWidth}px` }"
  >
    <div class="column-header">
      <h3>{{ columnData.model }}</h3>
      <div class="stats">
        <span>{{ columnData.totalCorrect }} / {{ store.totalExecutions }}</span>
      </div>
    </div>

    <div class="responses-container">
      <div v-if="columnData.state === 'loading'" class="loading-indicator">
        <div class="spinner"></div>
        <span>Processing...</span>
      </div>

      <div v-else-if="columnData.state === 'error'" class="error-message">
        <span>{{ columnData.responses[0]?.error }}</span>
        <button @click="$emit('retry', columnData.model)">Retry</button>
      </div>

      <template v-else>
        <div v-for="(response, index) in columnData.responses" :key="index" class="response-card">
          <div class="thought-section">
            <div class="section-header">
              <h4>Thoughts</h4>
              <button @click="copyToClipboard(response.thoughts)" class="copy-button">Copy</button>
            </div>
            <div class="content" :style="{ maxHeight: responseHeight + 'px' }">
              {{ response.thoughts || 'No thoughts provided' }}
            </div>
          </div>

          <div class="response-section">
            <div class="section-header">
              <h4>Response</h4>
              <button @click="copyToClipboard(response.response)" class="copy-button">Copy</button>
            </div>
            <div class="content" :style="{ maxHeight: responseHeight + 'px' }">
              {{ response.response }}
            </div>
          </div>
        </div>
      </template>
    </div>
  </div>
</template>

<script setup lang="ts">
import { store } from '../../stores/thoughtBenchStore';
import type { ThoughtBenchColumnData } from '../../types';
import { copyToClipboard } from '../../utils';

defineProps<{
  columnData: ThoughtBenchColumnData;
  responseHeight: number;
}>();

defineEmits<{
  (e: 'retry', model: string): void;
}>();
</script>

<style scoped>
.thought-column {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 1rem;
  background: white;
  transition: all 0.3s ease;
  flex-shrink: 0;
}

.thought-column.loading {
  opacity: 0.7;
}

.thought-column.error {
  border-color: #ff4444;
}

.column-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid #eee;
}

.column-header h3 {
  margin: 0;
  font-size: 1rem;
  color: #333;
}

.stats {
  font-size: 0.9rem;
  color: #666;
}

.responses-container {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  min-width: 100%;
}

.response-card {
  border: 1px solid #eee;
  border-radius: 4px;
  overflow: hidden;
}

.thought-section, .response-section {
  padding: 0.5rem;
}

.thought-section {
  background: #f8f9fa;
  border-bottom: 1px solid #eee;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.section-header h4 {
  margin: 0;
  font-size: 0.9rem;
  color: #666;
}

.content {
  overflow-y: auto;
  white-space: pre-wrap;
  font-family: monospace;
  font-size: 0.9rem;
  line-height: 1.4;
  padding: 0.5rem;
  background: white;
  border-radius: 4px;
}

.copy-button {
  padding: 2px 8px;
  font-size: 0.8rem;
  background: #eee;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.copy-button:hover {
  background: #ddd;
}

.loading-indicator {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  padding: 2rem;
}

.spinner {
  width: 30px;
  height: 30px;
  border: 3px solid #f3f3f3;
  border-top: 3px solid #3498db;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

.error-message {
  color: #ff4444;
  text-align: center;
  padding: 1rem;
}

.error-message button {
  margin-top: 0.5rem;
  padding: 0.5rem 1rem;
  background: #ff4444;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.error-message button:hover {
  background: #ff3333;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>
