# CLAUDE.md

## General Guidelines

回答は常に**日本語**で行ってください。
Your response must written by **Japanese**.

## Coding rules

### Basic rules

- Indentation: 2 spaces
- Indentation: 4 spaces (only Python, Ruby)

### Language-specific rules

- JavaScript/Typescript: ESlint + Prettier
- Python: PEP8
- Ruby: Rubocop
- Go: gofmt
- Rust: rustfmt + Clippy

## Workflow

- Be sure to typecheck when you’re done making a series of code changes
- Prefer running single tests, and not the whole test suite, for performance

### Test-Driven Development

- Proceed with test-driven development (TDD) as a general rule
- First create tests based on expected input and output
- Do not write implementation code, prepare only tests
- Run tests and check for failures
- Commit once you have confirmed that the tests are correct
- Then proceed with implementation to make the tests pass
- Do not change the tests during implementation, but continue to modify the code
- Repeat until all tests pass
