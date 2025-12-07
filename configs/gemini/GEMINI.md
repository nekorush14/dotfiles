# GEMINI.md

Your response must written in **Japanese**.

## Work Persistence

Your context window will be automatically compacted as it approaches its limit, allowing you to continue working indefinitely from where you left off.
Therefore:

- Do not stop tasks early due to token budget concerns
- Save current progress if approaching the limit
- Always complete tasks fully and autonomously

## Workflow & Process

- **TDD (Test Driven Development):**
  - **Pre-requisite:** Do NOT generate implementation code immediately
  - **Phase 1 (Red):** Outline or write the failing test case first
  - **Phase 2 (Green):** Write minimal code to satisfy the test
  - **Phase 3 (Refactor):** Optimize code structure
- **Verification:**
  - Always verify changes with available tests
  - If tests fail, analyze the root cause _before_ attempting a fix
- **Git**:
  - Follow conventional commit style: `<type>(<scope>): <description>`
  - Prefer `gh` command for GitHub operations
  - Write code comments in English
  - One commit per logical change
  - Create new reverting commit instead of rewriting history
  - Always specify origin and branch: `git push <origin> <branch>`

## Writing

- **When writing in Japanese, follow these rules**:
  - Insert a half-width space between half-width alphanumeric characters and full-width characters
  - Always use half-width punctuation marks (e.g., parentheses (), exclamation/question marks (!, ?), colons (:))
  - When creating or editing a file, it must always end with a newline character to avoid the “No newline at end of file” warning.

## Universal Safety Standards

- **Secrets:** NEVER output hardcoded API keys or passwords. Suggest environment variables.
- **Commands:** When suggesting shell commands, ensure they are non-destructive or include warnings.

## Universal Coding Style

- **Naming:** Use clear, purpose-revealing variable names
- **Comments:** Explain "Why" logic is complex, not "What" the code does.
