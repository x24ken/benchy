<template>
  <div class="container">
    <h1>ISO Speed Bench</h1>
    <div 
      class="file-drop" 
      @dragover.prevent 
      @drop="handleFileDrop"
      :class="{ loading: store.isLoading }"
      :aria-busy="store.isLoading"
    >
      <div v-if="store.isLoading" class="loading-content">
        <div class="loading-spinner"></div>
        <p>Running benchmarks... Please wait</p>
      </div>
      <p v-else>Drag & Drop YAML file here</p>
    </div>

    <div v-if="store.benchmarkResults.length > 0">
      <button @click="startBenchmark">Replay Bench</button>
      <button @click="resetBenchmark">Reset</button>

      <div class="speed-control">
        <label>Speed (ms):</label>
        <input type="number" v-model="store.speed" min="10" max="1000" />
      </div>

      <IsoSpeedBenchRow
        v-for="(result, index) in store.benchmarkResults"
        :key="index"
        :result="result"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import {
  store,
  resetBenchmark,
  startBenchmark,
} from "../stores/isoSpeedBenchStore";
import IsoSpeedBenchRow from "../components/IsoSpeedBenchRow.vue";

function handleFileDrop(event: DragEvent) {
  const file = event.dataTransfer?.files[0];
  if (file && (file.name.endsWith(".yaml") || file.name.endsWith(".yml"))) {
    const reader = new FileReader();
    reader.onload = async (e) => {
      const content = e.target?.result;
      if (typeof content === "string") {
        try {
          store.isLoading = true;
          const response = await fetch("/iso-speed-bench", {
            method: "POST",
            headers: {
              "Content-Type": "application/yaml",
            },
            body: content,
          });
          store.benchmarkResults = await response.json();
        } catch (error) {
          console.error("Error running benchmark:", error);
        } finally {
          store.isLoading = false;
        }
      }
    };
    reader.readAsText(file);
  }
}
</script>

<style scoped>
.container {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.file-drop {
  border: 2px dashed #ccc;
  padding: 20px;
  text-align: center;
  margin: 20px 0;
  cursor: pointer;
  min-height: 120px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
}

.file-drop.loading {
  border-color: #666;
  background-color: #f5f5f5;
  cursor: wait;
}

.loading-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
}

.speed-control {
  margin: 20px 0;
}

.loading-spinner {
  border: 3px solid rgba(0, 0, 0, 0.1);
  border-top: 3px solid #3498db;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>
