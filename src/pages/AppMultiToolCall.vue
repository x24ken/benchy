<template>
  <div class="container">
    <h1>Tool Call Prompt Benchmark</h1>
    <div class="tabs-container">
      <div class="tabs">
        <button
          :class="{ active: store.activeTab === 'toolcall' }"
          @click="store.activeTab = 'toolcall'"
        >
          Tool Call
        </button>
        <button
          :class="{ active: store.activeTab === 'notes' }"
          @click="store.activeTab = 'notes'"
        >
          Notes
        </button>
      </div>
      <div class="state-controls">
        <button class="state-button save" @click="saveState">Save</button>
        <button class="state-button reset" @click="resetState">Reset</button>
      </div>
    </div>

    <div class="tab-content">
      <div v-if="store.activeTab === 'toolcall'" class="tool-call-content">
        <ToolCallInputField />
        <ToolCallExpectationList />
        <button 
          @click="runToolCall" 
          class="run-button"
          :disabled="store.isLoading"
        >
          Run Tool Calls
        </button>
        <ToolCallTable />
      </div>
      <ToolCallNotesTab v-else />
    </div>
  </div>
</template>

<script setup lang="ts">
import ToolCallTab from "../components/multi_tool_call/ToolCallTab.vue";
import ToolCallNotesTab from "../components/multi_tool_call/ToolCallNotesTab.vue";
import ToolCallInputField from "../components/multi_tool_call/ToolCallInputField.vue";
import ToolCallExpectationList from "../components/multi_tool_call/ToolCallExpectationList.vue";
import ToolCallTable from "../components/multi_tool_call/ToolCallTable.vue";
import { store, resetState } from "../stores/toolCallStore";
import { runToolCall } from "../apis/toolCallApi";

function saveState() {
  localStorage.setItem("toolCallState", JSON.stringify(store));
}

document.title = "Tool Call Prompt Benchmark";
</script>

<style scoped>
.container {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

h1 {
  margin-bottom: 20px;
  color: rgb(14, 68, 145);
}

.tabs-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  border-bottom: 1px solid #e0e0e0;
}

.tabs {
  display: flex;
}

.tabs button {
  padding: 10px 20px;
  margin-right: 10px;
  border: none;
  background: none;
  cursor: pointer;
  font-size: 16px;
  color: #666;
}

.tabs button.active {
  color: rgb(14, 68, 145);
  border-bottom: 2px solid rgb(14, 68, 145);
}

.state-controls {
  display: flex;
  gap: 10px;
}

.state-button {
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.2s;
  color: white;
}

.state-button.save {
  background-color: rgb(14, 68, 145);
}

.state-button.save:hover {
  background-color: rgb(11, 54, 116);
}

.state-button.reset {
  background-color: rgb(145, 14, 14);
}

.state-button.reset:hover {
  background-color: rgb(116, 11, 11);
}

.tool-call-content {
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
<template>
  <div class="container">
    <h1>Tool Call Prompt Benchmark</h1>
    <div class="tabs-container">
      <div class="tabs">
        <button
          :class="{ active: store.activeTab === 'toolcall' }"
          @click="store.activeTab = 'toolcall'"
        >
          Tool Call
        </button>
        <button
          :class="{ active: store.activeTab === 'notes' }"
          @click="store.activeTab = 'notes'"
        >
          Notes
        </button>
      </div>
      <div class="state-controls">
        <button class="state-button save" @click="saveState">Save</button>
        <button class="state-button reset" @click="resetState">Reset</button>
      </div>
    </div>

    <div class="tab-content !w-1200px">
      <ToolCallTab v-if="store.activeTab === 'toolcall'" />
      <ToolCallNotesTab v-else />
    </div>
  </div>
</template>

<script setup lang="ts">
import ToolCallTab from "../components/multi_tool_call/ToolCallTab.vue";
import ToolCallNotesTab from "../components/multi_tool_call/ToolCallNotesTab.vue";
import { store, resetState } from "../stores/toolCallStore";

function saveState() {
  localStorage.setItem("toolCallState", JSON.stringify(store));
}

document.title = "Tool Call Prompt Benchmark";
</script>

<style scoped>
.container {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

h1 {
  margin-bottom: 20px;
  color: rgb(14, 68, 145);
}

.tabs-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  border-bottom: 1px solid #e0e0e0;
}

.tabs {
  display: flex;
}

.tabs button {
  padding: 10px 20px;
  margin-right: 10px;
  border: none;
  background: none;
  cursor: pointer;
  font-size: 16px;
  color: #666;
}

.tabs button.active {
  color: rgb(14, 68, 145);
  border-bottom: 2px solid rgb(14, 68, 145);
}

.state-controls {
  display: flex;
  gap: 10px;
}

.state-button {
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.2s;
  color: white;
}

.state-button.save {
  background-color: rgb(14, 68, 145);
}

.state-button.save:hover {
  background-color: rgb(11, 54, 116);
}

.state-button.reset {
  background-color: rgb(145, 14, 14);
}

.state-button.reset:hover {
  background-color: rgb(116, 11, 11);
}

.tab-content {
  flex: 1;
  min-height: 0;
}
</style>
