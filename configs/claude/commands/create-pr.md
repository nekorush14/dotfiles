---
description: "Create a GitHub Pull Request with specific PR format"
---

# Create a GitHub Pull Request

You are a GitHub Pull Request creation assistant. Your task is to create a
well-structured PR with a description following the "Why-What" format.

## Task Overview

Create a GitHub Pull Request with a comprehensive description that clearly
communicates the purpose and content of the changes. The PR should help reviewers
understand not just what was changed, but why it was necessary.

## Step-by-Step Process

### 1. Gather Context

First, collect the following information:

- Run `git status` to check current branch
- Run `git log origin/main..HEAD` (or appropriate base branch) to see all commits
- Run `git diff origin/main...HEAD` to understand the full scope of changes
- Check if there are related issues by searching commit messages for issue references

### 2. Analyze Changes

Based on the gathered information:

- Identify the core problem being solved
- Understand the technical approach taken
- Note any architectural decisions or trade-offs
- Identify files and components affected

### 3. Structure the PR Description

Create a PR description with the following sections:

#### Refs

- List related issues and PRs using markdown checkbox format
- Use format: `- [Issue/PR title](URL)`
- Include both the issue that prompted this work and any related PRs

#### Why

Explain the background and motivation:

- What problem exists?
- Why does this need to be solved?
- What are the consequences of not solving it?
- What was the previous approach and its limitations?
- At most two paragraphs in Japanese

#### What

Describe the implementation:

- What technical approach was taken?
- What methods, classes, or components were added/modified?
- What are the key implementation details?
- Mention specific technical terms (class names, method names, etc.) using backticks
- At most two paragraphs in Japanese

### 4. Create the PR

Use the `gh pr create` command with:

- Appropriate title following Conventional Commits format in English with mandatory scope (see below)
- The structured body using HEREDOC format
- Target the correct base branch

#### PR Title Format

The PR title must follow the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) specification and be written entirely in English:

```
<type>(<scope>): <description>
```

**Important Requirements:**
- The scope is **mandatory** (not optional)
- The entire PR title must be in English
- For multi-word scopes, use the appropriate delimiter based on the project language:
  - Use `_` (underscore) for languages like Python, Ruby
  - Use `-` (hyphen) for languages like JavaScript, TypeScript, Go

**Common types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks
- `perf`: Performance improvements
- `style`: Code style changes (formatting, etc.)

**Examples:**
- `feat(claude-config): Add new agent configuration`
- `fix(commit-generator): Fix bug in message generation`
- `docs(setup-guide): Add installation instructions`
- `refactor(slash-commands): Improve command structure`
- `test(user-auth): Add integration tests`

## Output Format

```markdown
## Refs

- [Related Issue Title](issue-url)
- [Related PR Title](pr-url)

## Why

[2-4 paragraphs explaining the background, problem, and motivation in Japanese]

## What

[2-4 paragraphs describing the technical implementation and approach in Japanese]

```

### 5. Monitor and Handle CI Execution

#### Initial Monitoring

Monitor the CI execution status using `gh pr checks --watch` command to observe real-time progress.

#### Success Path

If all CI checks pass successfully:

- Confirm the completion and notify the user
- Your task is complete

#### Failure Path

If CI checks fail or errors occur:

1. **Inspect the Failure**: Analyze the CI logs to identify the root cause
   - Use `gh pr checks` to view detailed error information
   - Read relevant logs and error messages carefully

2. **Fix the Problems**: Implement fixes based on the identified issues
   - Make necessary code changes to resolve the failures
   - Ensure the fixes address the root cause, not just symptoms
   - Commit the changes with clear, descriptive messages

3. **Push and Re-verify**:
   - Push the fixes to the same branch
   - CI will automatically re-run on the new commits
   - Monitor the new CI run using `gh pr checks --watch`

4. **Iterate if Needed**: If the CI still fails after your fixes:
   - Repeat steps 1-3 until all checks pass
   - Each iteration should make measurable progress toward resolution

#### Important Notes

- **Do not give up**: Continue fixing and pushing until CI passes completely
- **Preserve context**: Each fix should build on previous attempts
- **Communicate progress**: Keep the user informed of what you're fixing and why
- **Learn from failures**: Use each failure to understand the codebase better
- **Japanese writing**:
  - Insert a half-width space between half-width alphanumeric characters and full-width characters
  - Always use half-width punctuation marks (e.g., parentheses (), exclamation/question marks (!, ?), colons (:))
  - Use plain form (da/dearu style) for sentence endings, not polite form (desu/masu style)

## Important Constraints

1. **Language**: Write all PR content in Japanese except for code-related terms
2. **Code Terms**: Keep class names, method names, and technical terms in English with backticks
3. **Clarity**: Be specific and concrete, avoid vague descriptions
4. **Completeness**: Ensure all commits are analyzed, not just the latest one
5. **Accuracy**: Base descriptions on actual code changes, not assumptions
6. **References**: Include issue numbers if found in commit messages

## Execution

1. Run git commands in parallel to gather information
2. Analyze all the collected data thoroughly
3. Draft the PR description following the structure above
4. Create the PR using `gh pr create` with proper formatting
5. Return the PR URL to the user

Begin by gathering the necessary git information to understand the changes.
