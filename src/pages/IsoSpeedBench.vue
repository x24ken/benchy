<template>
  <div class="container">
    <h1>ISO Speed Bench</h1>
    
    <div v-if="!store.benchmarkReport">
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

      <button 
        @click="useSampleData"
        class="sample-data-button"
      >
        Or use sample data
      </button>
    </div>

    <div v-else class="benchmark-container">
      <div class="controls">
        <button @click="startBenchmark">Replay Bench</button>
        <button @click="fullReset">Reset</button>

        <div class="speed-control">
          <label>Speed (ms):</label>
          <input type="number" v-model="store.speed" min="10" max="1000" />
        </div>
      </div>

      <IsoSpeedBenchRow
        v-for="(modelReport, index) in store.benchmarkReport.models"
        :key="index"
        :modelReport="modelReport"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import {
  store,
  resetBenchmark,
  startBenchmark,
  inMemoryBenchmarkReport,
} from "../stores/isoSpeedBenchStore";
import IsoSpeedBenchRow from "../components/IsoSpeedBenchRow.vue";

function useSampleData() {
  store.benchmarkReport = inMemoryBenchmarkReport;
}

function fullReset() {
  resetBenchmark();
  store.benchmarkReport = null;
}

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
          store.benchmarkReport = await response.json();
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
  max-width: 80vw;
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

.sample-data-button {
  padding: 10px 20px;
  background-color: #3498db;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin-bottom: 20px;
  transition: background-color 0.3s ease;
}

.sample-data-button:hover {
  background-color: #2980b9;
}

.loading-spinner {
  border: 3px solid rgba(0, 0, 0, 0.1);
  border-top: 3px solid #3498db;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
}

.controls {
  margin-bottom: 20px;
  display: flex;
  gap: 10px;
  align-items: center;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
</style>
