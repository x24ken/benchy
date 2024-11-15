<template>
  <div class="toolcallexpectationlist-w">
    <div class="tool-selector">
      <select v-model="selectedTool" @change="addToolCall">
        <option value="">Select a tool</option>
        <option v-for="tool in allTools" :key="tool" :value="tool">
          {{ tool }}
        </option>
      </select>
      <ToolCallExpectationRandomizer />
    </div>
    <div class="tool-tags">
      <div
        v-for="(tool, index) in store.expectedToolCalls"
        :key="index"
        class="tool-tag"
        :style="{ backgroundColor: stringToColor(tool) }"
      >
        {{ tool }}
        <button @click="removeToolCall(index)" class="remove-tag">×</button>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref } from "vue";
import { store } from "../../stores/toolCallStore";
import { allTools } from "../../utils";
import ToolCallExpectationRandomizer from "./ToolCallExpectationRandomizer.vue";
function stringToColor(str: string): string {
  // Generate hash from string
  let hash = 0;
  for (let i = 0; i < str.length; i++) {
    hash = str.charCodeAt(i) + ((hash << 5) - hash);
  }

  // Convert to HSL to ensure visually distinct colors
  const h = Math.abs(hash) % 360; // Hue: 0-360
  const s = 50 + (Math.abs(hash) % 40); // Saturation: 50-90%
  const l = 20 + (Math.abs(hash) % 25); // Lightness: 20-45%

  // Add secondary hue rotation for more variation
  const h2 = (h + 137) % 360; // Golden angle rotation
  const finalHue = hash % 2 === 0 ? h : h2;

  return `hsl(${finalHue}, ${s}%, ${l}%)`;
}

const selectedTool = ref("");

function addToolCall() {
  if (selectedTool.value) {
    store.expectedToolCalls.push(selectedTool.value);
    selectedTool.value = ""; // Reset selection
  }
}

function removeToolCall(index: number) {
  store.expectedToolCalls.splice(index, 1);
}
</script>

<style scoped>
.toolcallexpectationlist-w {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
.tool-selector {
  display: flex;
  gap: 1rem;
  align-items: flex-start;
}
.tool-selector select {
  width: 200px;
  padding: 0.5rem;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.tool-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.tool-tag {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.25rem 0.5rem;
  color: white;
  border-radius: 4px;
}

.remove-tag {
  background: none;
  border: none;
  color: white;
  cursor: pointer;
  padding: 0;
  font-size: 1.2rem;
  line-height: 1;
}

.remove-tag:hover {
  opacity: 0.8;
}
</style>
