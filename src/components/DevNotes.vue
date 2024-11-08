<template>
  <div class="notes-container">
    <ul>
      <li>
        This is a micro-application for benchmarking different LLM models on
        autocomplete tasks
      </li>
      <li>
        Supports multiple models:
        <ul>
          <li>
            Claude Models:
            <ul>
              <li>haiku</li>
              <li>sonnet</li>
            </ul>
          </li>
          <li>
            Gemini Models:
            <ul>
              <li>gemini_pro_2</li>
              <li>gemini_flash_2</li>
              <li>gemini_flash_8b</li>
            </ul>
          </li>
          <li>
            GPT Models:
            <ul>
              <li>gpt_4o</li>
              <li>gpt_4o_mini</li>
              <li>gpt_4o_predictive</li>
              <li>gpt_4o_mini_predictive</li>
            </ul>
          </li>
        </ul>
      </li>
      <li>
        Features:
        <ul>
          <li>Real-time code input with syntax highlighting</li>
          <li>Customizable prompt template</li>
          <li>Response time measurements</li>
          <li>Execution cost tracking</li>
          <li>State persistence with save/reset functionality</li>
        </ul>
      </li>
      <li>Uses Vue 3 with TypeScript</li>
      <li>Grid implementation using AG Grid</li>
      <li>Code editor using CodeMirror 6</li>
      <li>Styling with UnoCSS</li>
      <li>
        Known Limitations:
        <ul>
          <li>
            Network latency to LLM provider servers is not factored into
            performance measurements
          </li>
          <li>
            Cost calculations for Gemini models do not account for price
            increases after 128k tokens
          </li>
          <li>Cost calculations do not include caching costs</li>
          <li>
            Uses default settings in
            <a
              target="_blank"
              href="https://github.com/simonw/llm?tab=readme-ov-file"
              >LLM</a
            >
            and
            <a target="_blank" href="https://github.com/openai/openai-python"
              >OpenAI</a
            >
            libraries with streaming disabled - not utilizing response token
            limits or other performance optimization techniques
          </li>
        </ul>
      </li>
    </ul>
  </div>
</template>

<style scoped>
.notes-container {
  padding: 20px;
  max-width: 800px;
  margin: 0 auto;
}

ul {
  list-style-type: disc;
  margin-left: 20px;
  line-height: 1.6;
}

ul ul {
  margin-top: 10px;
  margin-bottom: 10px;
}

li {
  margin-bottom: 12px;
  color: #333;
}
</style>
