# Initialize parallel git worktree setup

## Variables
FEATURE_NAME: $ARGUMENTS
NUMBER_OF_PARALLEL_WORKTREES: $ARGUMENTS

## Run these commands top to bottom

- create a new dir `trees/`
- for i in NUMBER_OF_PARALLEL_WORKTREES
  - run `git worktree -b <FEATURE_NAME>-<i> ./trees/<FEATURE_NAME>-<i>`
  - run `cp server/.env ./trees/<FEATURE_NAME>-<i>/server/.env`
  - run `cd server`, `uv sync`
  - run `cd ../client`, `bun i`
  - run `cd ../`, `./start.sh`
  - run `cd trees/<FEATURE_NAME>-<i>`, `git ls-files` to validate
