---
description: "Create a GitHub Pull Request with specific PR format"
---

# Create a GitHub Pull Request

Your task is to create a GitHub Pull Request with specific PR format.
Your outputs must write by Japanese.
You must follow the flow section.

## Flow

1. Create a Pull Request using `gh pr create` command
2. Watch the status of the CI execution

### 1. Create a Pull Request using `gh pr create` command

You must use following format to create PR as PR description.
Write the "Why" and "What" in your PR description in sentences, not bullet points.
Write all "what" in the present tense.

**IMPORTANT**: Use appropriate line breaks to make it easy to read.
**IMPORTANT**: End sentences in the plain style, not the polite style.

```markdown
## Why

- Explain the purpose and background to anser why this PR will needed
  - Explanation must containing the background of this change or fixing with reference of issues for any other past problems

## What

- Describe the overall summarized changes and impacts for present tense instead of individual commits.
- Add `🤖 Generated with Claude Code` at the end
```

### 2. Watch the status of the CI execution

You watch the status of the CI execution using `gh pr checks --watch` command.
If CI done successfully, your task has also been completed.
If CI has failed or occurring the errors, inspect it and fix the problems, then push again.
