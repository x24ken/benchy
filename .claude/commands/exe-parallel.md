# Parallel Task Version Execution

## Variables
PLAN_TO_EXECUTE: $ARGUMENTS
NUMBER_OF_PARALLEL_WORKTREES: $ARGUMENTS

## Run these commands top to bottom
RUN `eza server --tree --git-ignore`
RUN `eza client --tree --git-ignore`
RUN `eza trees --tree --level 3`
READ: PLAN_TO_EXECUTE

## Instructions

We're going to create NUMBER_OF_PARALLEL_WORKTREES new subagents that run in parallel using Batch -> [Task, Task, ...] in their own version of this git repo.

The first agent will run in trees/<predefined_feature_name>-1/
The second agent will run in trees/<predefined_feature_name>-2/
...
The last agent will run in trees/<predefined_feature_name>-<NUMBER_OF_PARALLEL_WORKTREES>/

Each agent will independently implement the engineering plan detailed in PLAN_TO_EXECUTE

When prompting the subagent, have them report their final changes made in a comprehensive `RESULTS.md` file at the root of their respective workspace.

Be sure each subagent first pulls and merges changes from our current branch - pass the branch into each subagent prompt.