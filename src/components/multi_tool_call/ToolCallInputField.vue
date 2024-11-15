<template>
  <div class="toolcallinputfield-w">
    <code-mirror
      v-model="store.userInput"
      :basic="true"
      class="editor !h-100px !w-full"
      placeholder="Enter your prompt for tool calls..."
    />
  </div>
</template>

<script lang="ts" setup>
import CodeMirror from "vue-codemirror6";
import { store } from "../../stores/toolCallStore";
</script>

<style scoped>
.toolcallinputfield-w {
  width: 100%;
}

.editor {
  width: 100%;
  font-family: "Monaco", "Menlo", "Ubuntu Mono", "Consolas", monospace;
  background-color: #f5f5f5;
}

:deep(.cm-editor) {
  height: 100%;
}

:deep(.cm-scroller) {
  overflow: auto;
}
</style>
