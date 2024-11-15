<template>
  <div class="toolcalltab-w">
    <ToolCallInputField />
    <div style="display: flex; gap: 1rem; align-items: flex-start;">
      <ToolCallExpectationList />
    </div>
    <button 
      @click="runToolCall" 
      class="run-button"
      :disabled="store.isLoading"
    >
      {{ store.isLoading ? 'Running...' : 'Run Tool Calls' }}
    </button>
    <ToolCallTable />
  </div>
</template>

<script lang="ts" setup>
import ToolCallInputField from "./ToolCallInputField.vue";
import ToolCallExpectationList from "./ToolCallExpectationList.vue";
import ToolCallTable from "./ToolCallTable.vue";
import { store } from "../../stores/toolCallStore";
import { runToolCall } from "../../apis/toolCallApi";
</script>

<style scoped>
.toolcalltab-w {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.run-button {
  background-color: rgb(14, 68, 145);
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
  align-self: flex-start;
}

.run-button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}
</style>
