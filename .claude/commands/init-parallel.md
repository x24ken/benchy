# Initialize parallel git worktree directories

## Variables
FEATURE_NAME: $ARGUMENTS
NUMBER_OF_PARALLEL_WORKTREES: $ARGUMENTS

## Run these commands top to bottom

- create a new dir `trees/`
- for i in NUMBER_OF_PARALLEL_WORKTREES
  - RUN `git worktree add -b <FEATURE_NAME>-<i> ./trees/<FEATURE_NAME>-<i>`
  - RUN `cp ./server/.env ./trees/<FEATURE_NAME>-<i>/server/.env`
  - RUN `cd ./trees/<FEATURE_NAME>-<i>/server`, `uv sync`
  - RUN `cd ../client`, `bun i`
  - UPDATE `./trees/<FEATURE_NAME>-<i>/server/server.py`: 
    - `app.run(debug=True, port=5000+(i))`
  - UPDATE `./trees/<FEATURE_NAME>-<i>/client/vite.config.ts`: 
    - `port: 5173+(i),`
    - `proxy target: 'http://127.0.0.1:500'+(i)`
  - RUN `cd trees/<FEATURE_NAME>-<i>`, `git ls-files` to validate
  - RUN `cat ./trees/<FEATURE_NAME>-<i>/server/server.py` to verify the port is set correctly for the current worktree
  - RUN `cat ./trees/<FEATURE_NAME>-<i>/client/vite.config.ts` to verify the client + server proxy port is set correctly for the current worktree
- RUN `git worktree list` to verify all trees were created properly