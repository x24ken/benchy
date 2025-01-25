<template>
  <div class="container">
    <h1 v-if="store.settings.modelStatDetail !== 'hide'">Thought Bench</h1>

    <div
      class="benchmark-info"
      v-if="store.settings.modelStatDetail !== 'hide'"
    >
      <p>
        Analyze model reasoning processes and response quality through
        structured thought visualization.
      </p>
    </div>

    <div class="controls">
      <button
        @click="runBenchmark"
        :disabled="store.apiCallInProgress || isAnyColumnLoading"
      >
        {{ runButtonText }}
      </button>
      <button @click="clickResetState">Reset</button>
      <button @click="showSettings = !showSettings">
        {{ showSettings ? "Hide" : "Show" }} Settings
      </button>

      <div v-if="showSettings" class="settings-row">
        <div class="setting">
          <label>Model Stats:</label>
          <select v-model="store.settings.modelStatDetail">
            <option value="verbose">Verbose</option>
            <option value="hide">Hide</option>
          </select>
        </div>
        <div class="setting">
          <label>Column Height:</label>
          <input
            type="range"
            v-model.number="store.settings.columnHeight"
            min="100"
            max="1500"
            class="slider"
          />
          <span>{{ store.settings.columnHeight }}px</span>
        </div>
        <div class="setting">
          <label>Column Width:</label>
          <input
            type="range"
            v-model.number="store.settings.columnWidth"
            min="200"
            max="1500"
            class="slider"
          />
          <span>{{ store.settings.columnWidth }}px</span>
        </div>
      </div>
    </div>

    <div class="prompt-area">
      <textarea
        v-model="store.prompt"
        @keydown.ctrl.enter.prevent="runBenchmark"
        @keydown.meta.enter.prevent="runBenchmark"
        placeholder="Enter your reasoning prompt..."
        class="prompt-input"
      ></textarea>
    </div>

    <div class="response-grid">
      <ThoughtColumn
        v-for="(column, index) in store.dataColumns"
        :key="index"
        :columnData="column"
        :columnHeight="store.settings.columnHeight"
        @retry="runSingleBenchmark(column.model)"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from "vue";
import { store, resetState } from "../stores/thoughtBenchStore";

// Add reset handler
function clickResetState() {
  resetState();
}
import ThoughtColumn from "../components/thought_bench/ThoughtColumn.vue";
import { runThoughtPrompt } from "../apis/thoughtBenchApi";

const showSettings = ref(false);

const isAnyColumnLoading = computed(() =>
  store.dataColumns.some((c) => c.state === "loading")
);

const runButtonText = computed(() => {
  if (store.apiCallInProgress) {
    const runningCount = store.dataColumns.filter(
      (c) => c.state === "loading"
    ).length;
    return `Running (${runningCount}/${store.dataColumns.length})`;
  }
  return "Run Benchmark";
});

async function runBenchmark() {
  if (store.apiCallInProgress || isAnyColumnLoading.value) return;

  store.apiCallInProgress = true;
  try {
    const promises = store.dataColumns.map((column) =>
      runSingleBenchmark(column.model)
    );
    await Promise.allSettled(promises);
  } finally {
    store.apiCallInProgress = false;
  }
}

async function runSingleBenchmark(model: string) {
  const column = store.dataColumns.find((c) => c.model === model);
  if (!column || column.state === "loading") return;

  try {
    column.state = "loading";
    store.totalExecutions++;
    const response = await runThoughtPrompt({
      prompt: store.prompt,
      model: model,
    });

    column.responses.unshift(response);
    if (!response.error) column.totalCorrect++;
    column.state = "success";
  } catch (error) {
    console.error(`Error running benchmark for ${model}:`, error);
    column.responses.unshift({
      thoughts: "",
      response: `Error: ${(error as Error).message}`,
      error: (error as Error).message,
    });
    column.state = "error";
  } finally {
    column.state = "idle";
  }
}
</script>

<style scoped>
.container {
  padding: 20px;
  max-width: 95vw;
  min-width: 70vw;
  margin: 0 auto;
}

h1 {
  font-size: 2.5rem;
  background: linear-gradient(90deg, #0e4491 0%, #00d4ff 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  text-align: center;
  margin-bottom: 1rem;
}

.benchmark-info {
  margin-bottom: 2rem;
  text-align: center;
  color: #666;
}

.prompt-area {
  margin: 2rem 0;
}

.prompt-input {
  width: 100%;
  height: 150px;
  padding: 1rem;
  border: 2px solid #ccc;
  border-radius: 8px;
  font-family: monospace;
  resize: vertical;
}

.response-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  margin-top: 2rem;
}

.controls {
  margin-bottom: 2rem;
  display: flex;
  gap: 1rem;
  align-items: center;
}

.settings-row {
  display: flex;
  gap: 2rem;
  padding: 1rem;
  background: #f5f5f5;
  border-radius: 8px;
  margin-top: 1rem;
}

.setting {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.slider {
  width: 100px;
}

button {
  padding: 0.5rem 1rem;
  background: #e0e0e0;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background 0.2s;
}

button:hover {
  background: #d0d0d0;
}

button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
  background: #f0f0f0;
}

button:disabled:hover {
  background: #f0f0f0;
}

.prompt-input:focus {
  outline: 2px solid #0e4491;
}
</style>
