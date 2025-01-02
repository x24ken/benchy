<template>
  <div class="container">
    <h1>ISO Speed Bench</h1>
    <div class="file-drop" @dragover.prevent @drop="handleFileDrop">
      <p>Drag & Drop YAML file here</p>
    </div>
    
    <div v-if="store.benchmarkResults.length > 0">
      <button @click="startBenchmark">Replay Bench</button>
      <button @click="resetBenchmark">Reset</button>
      
      <div class="speed-control">
        <label>Speed (ms):</label>
        <input type="number" v-model="store.speed" min="10" max="1000">
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
import { store, resetBenchmark, startBenchmark } from "../stores/isoSpeedBenchStore";
import IsoSpeedBenchRow from "../components/IsoSpeedBenchRow.vue";

function handleFileDrop(event: DragEvent) {
  const file = event.dataTransfer?.files[0];
  if (file && file.name.endsWith('.yaml')) {
    const reader = new FileReader();
    reader.onload = async (e) => {
      const content = e.target?.result;
      if (typeof content === 'string') {
        try {
          store.isLoading = true;
          const response = await fetch('/iso-speed-bench', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/yaml',
            },
            body: content,
          });
          store.benchmarkResults = await response.json();
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
}

.speed-control {
  margin: 20px 0;
}
</style>
