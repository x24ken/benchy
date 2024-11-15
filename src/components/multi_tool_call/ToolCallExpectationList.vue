<template>
  <div class="toolcallexpectationlist-w">
    <div class="tool-selector">
      <select v-model="selectedTool" @change="addToolCall">
        <option value="">Select a tool</option>
        <option v-for="tool in allTools" :key="tool" :value="tool">
          {{ tool }}
        </option>
      </select>
    </div>
    <div class="tool-tags">
      <div v-for="(tool, index) in store.expectedToolCalls" :key="index" class="tool-tag">
        {{ tool }}
        <button @click="removeToolCall(index)" class="remove-tag">×</button>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue';
import { store } from "../../stores/toolCallStore";

// Import from server/modules/tools.py
const allTools = ["run_coder_agent", "run_git_agent", "run_docs_agent"];
const selectedTool = ref('');

function addToolCall() {
  if (selectedTool.value) {
    store.expectedToolCalls.push(selectedTool.value);
    selectedTool.value = ''; // Reset selection
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
  background-color: rgb(14, 68, 145);
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
