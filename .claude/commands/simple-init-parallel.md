# Simple Init Parallel

Initialize three parallel git worktree directories for concurrent development.

## Variables
FEATURE_NAME: $ARGUMENTS

## Execute these tasks

CREATE new directory `trees/`

> Execute these steps in parallel with the tool `Batch -> [Task, Task, Task]`

CREATE first worktree:
- RUN `git worktree add -b FEATURE_NAME-1 ./trees/FEATURE_NAME-1`
- COPY `./server/.env` to `./trees/FEATURE_NAME-1/server/.env`
- RUN `cd ./trees/FEATURE_NAME-1/server` then `uv sync`
- RUN `cd ../client` then `bun i`
- UPDATE `./trees/FEATURE_NAME-1/server/server.py` port to `5001`
- UPDATE `./trees/FEATURE_NAME-1/client/vite.config.ts` port to `5174` and proxy to `5001`

CREATE second worktree:
- RUN `git worktree add -b FEATURE_NAME-2 ./trees/FEATURE_NAME-2`
- COPY `./server/.env` to `./trees/FEATURE_NAME-2/server/.env`
- RUN `cd ./trees/FEATURE_NAME-2/server` then `uv sync`
- RUN `cd ../client` then `bun i`
- UPDATE `./trees/FEATURE_NAME-2/server/server.py` port to `5002`
- UPDATE `./trees/FEATURE_NAME-2/client/vite.config.ts` port to `5175` and proxy to `5002`

CREATE third worktree:
- RUN `git worktree add -b FEATURE_NAME-3 ./trees/FEATURE_NAME-3`
- COPY `./server/.env` to `./trees/FEATURE_NAME-3/server/.env`
- RUN `cd ./trees/FEATURE_NAME-3/server` then `uv sync`
- RUN `cd ../client` then `bun i`
- UPDATE `./trees/FEATURE_NAME-3/server/server.py` port to `5003`
- UPDATE `./trees/FEATURE_NAME-3/client/vite.config.ts` port to `5176` and proxy to `5003`

VERIFY setup by running `git worktree list`