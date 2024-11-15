<template>
  <div class="tool-randomizer">
    <select v-model="selectedCount" @change="handleSelection">
      <option value="">Randomize tool count...</option>
      <option value="reset">Clear list</option>
      <option v-for="count in toolCounts" :key="count" :value="count">
        Randomize {{ count }} tools
      </option>
    </select>
  </div>
</template>

<script lang="ts" setup>
import { ref } from "vue";
import { store } from "../../stores/toolCallStore";
import { allTools } from "../../utils";

const selectedCount = ref("");
const toolCounts = [3, 5, 7, 9, 11, 13, 15];

function handleSelection() {
  if (selectedCount.value === "reset") {
    store.expectedToolCalls = [];
  } else if (selectedCount.value) {
    const count = parseInt(selectedCount.value);
    const randomTools: string[] = [];

    // Create a copy of allTools to avoid modifying the original
    const availableTools = [...allTools];

    // Generate random selections
    while (randomTools.length < count && availableTools.length > 0) {
      const randomIndex = Math.floor(Math.random() * availableTools.length);
      randomTools.push(availableTools[randomIndex]);
    }

    store.expectedToolCalls = randomTools;
  }

  // Reset selection to placeholder
  selectedCount.value = "";
}
</script>

<style scoped>
.tool-randomizer select {
  width: 200px;
  padding: 0.5rem;
  border: 1px solid #ccc;
  border-radius: 4px;
}
</style>
