---
description: Create a pull request to contribute to this repository.
---
# Create PR

Your task is to create a pull request (PR) to contribute to this repository.
You must follow the flow section.

## Flow

1. You create body of pull request by execute `@~/.claude/commands/guidelines/pull-request.md`
2. You run `gh pr create --title <TITLE> --body <PR_BODY>`
3. Watch the status of the CI execution

## Watch the status of the CI execution

You watch the status of the CI execution using `gh pr checks --watch` command.
If CI done successfly, your task has also been completed.
If CI has failer or occuring the errors, inspect it and fix the probrems, then push again.
