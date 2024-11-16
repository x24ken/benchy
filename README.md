# BENCHY
> Benchmarks you can **feel**
> 
> Watch the walk through [video here](https://youtu.be/1ObiaSiA8BQ)

<img src="./images/perf-price-speed-pick-two.png" alt="pick-two" style="max-width: 800px;">

## Live Benchmark Tool
- [Multi Autocomplete](src/pages/AppMultiAutocomplete.vue)
  - Goal: Understand [claude 3.5 haiku](https://www.anthropic.com/claude/haiku) & GPT-4o [predictive outputs](https://platform.openai.com/docs/guides/predicted-outputs) compared to existing models. 
- [Long Tool Calling](src/pages/AppMultiToolCall.vue)
  - Goal: Understand the best LLMs and techniques for LONG chains of tool calls / function calls (15+).

## Important Files
- `.env` - Environment variables for API keys
- `server/.env` - Environment variables for API keys
- `package.json` - Front end dependencies
- `server/pyproject.toml` - Server dependencies
- `src/store/*` - Stores all front end state and prompt
- `src/api/*` - API layer for all requests
- `server/server.py` - Server routes
- `server/llm_models.py` - All LLM models

## Setup

### Get API Keys
- [Anthropic](https://docs.anthropic.com/en/api/getting-started)
- [Google Cloud](https://ai.google.dev/gemini-api/docs/api-key)
- [OpenAI](https://help.openai.com/en/articles/4936850-where-do-i-find-my-openai-api-key)

### Client Setup
```bash
# Install dependencies using bun (recommended)
bun install

# Or using npm
npm install

# Or using yarn
yarn install

# Start development server
bun dev  # or npm run dev / yarn dev
```

### Server Setup
```bash
# Move into server directory
cd server

# Create and activate virtual environment using uv
uv sync

# Set up environment variables
cp .env.sample .env

# Set EVERY .env key with your API keys and settings
ANTHROPIC_API_KEY=
OPENAI_API_KEY=
GEMINI_API_KEY=

# Start server
uv run python server.py

# Run tests
uv run pytest (**beware will hit APIs and cost money**)
```

## Dev Notes & Caveats
- See `src/components/DevNotes.vue` for limitations

## Resources
- https://github.com/simonw/llm?tab=readme-ov-file
- https://github.com/openai/openai-python
- https://platform.openai.com/docs/guides/predicted-outputs
- https://community.openai.com/t/introducing-predicted-outputs/1004502
- https://unocss.dev/integrations/vite
- https://www.npmjs.com/package/vue-codemirror6
- https://vuejs.org/guide/scaling-up/state-management
- https://www.ag-grid.com/vue-data-grid/getting-started/
- https://www.ag-grid.com/vue-data-grid/value-formatters/
- https://llm.datasette.io/en/stable/index.html
- https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/get-token-count
- https://ai.google.dev/gemini-api/docs/tokens?lang=python
- https://ai.google.dev/pricing#1_5flash
- https://ai.google.dev/gemini-api/docs/structured-output?lang=python
- https://platform.openai.com/docs/guides/structured-outputs
- https://docs.anthropic.com/en/docs/build-with-claude/tool-use
- https://ai.google.dev/gemini-api/docs/models/experimental-models