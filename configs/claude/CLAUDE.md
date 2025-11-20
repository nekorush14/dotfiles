# CLAUDE.md

## General Guidelines

回答は常に**日本語**で行ってください。
Your response must written by **Japanese**.

### Writing

When writing in Japanese, follow these rules:

- Insert a half-width space between half-width alphanumeric characters and full-width characters
- Always use half-width punctuation marks (e.g., parentheses (), exclamation/question marks (!, ?), colons (:))

## Coding rules

### Basic rules

- Indentation: 2 spaces
- Indentation: 4 spaces (only Python, Ruby)
- If you want to access GitHub, you must use the `gh` command instead of `GitHub MCP Searver`
- If you want to write code comment, you must write code comment by English
- If you want to write code comment, you must write code comment to explaine "WHY" instead of "WHAT" or "HOW"
- If you failed to run the cd command, use `/usr/bin/cd` command instead of `cd` command
- If you want to run `git push` command to push your changes, you must run `git push <ORIGIN_NAME> <BRANCH_NAME>` command instead of `git push -set-upstream <ORIGIN_NAME> <BRANCH_NAME>` command

### Language-specific rules

- JavaScript/Typescript: ESlint + Prettier
- Python: PEP8
- Ruby:
  - Linter/Formatter: `bundle exec rubocop`
  - Ruby command: `$HOME/.rbenv/shims/ruby`
  - Rails: `bundle exec rails`
- Go: gofmt
- Rust: rustfmt + Clippy

## Workflow

- Be sure to typecheck when you’re done making a series of code changes
- Prefer running single tests, and not the whole test suite, for performance
- You **DO NOT** revert past commits using git command
  - If you need to revert changes, you must create new REVERTING COMMIT
- Essentially, a commit should only contain one fix or one consistent change to a single feature
- You must follow the Test-Driven Development (TDD) approach to ensure code quality

### Test-Driven Development (TDD)

- Proceed with test-driven development (TDD) as a general rule
- First create tests based on expected input and output
- Do not write implementation code, prepare only tests
- Run tests and check for failures
- Commit once you have confirmed that the tests are correct
- Then proceed with implementation to make the tests pass
- Do not change the tests during implementation, but continue to modify the code
- Repeat until all tests pass
