# CLAUDE.md

State it simply and concisely.
Instead of making judgments based on speculation or guesswork, verify the code and execution results before reporting.
Do not omit or modify predetermined procedures.
Do not output like "Good question!", "良い指摘です", "良い質問です" or "That's a good point!" when responding to user questions or feedback.
Instead, provide direct and informative responses without unnecessary commentary.

## Writing
- Use tree symbols (e.g., `└─`, `├─`) only for directory structures or text-based diagrams when Mermaid is unavailable.
- **When writing in Japanese, follow these rules**:
  - Insert a half-width space between half-width alphanumeric characters and full-width characters
  - Always use half-width punctuation marks (e.g., parentheses (), exclamation/question marks (!, ?), colons (:))
  - When creating or editing a file, it must always end with a newline character to avoid the “No newline at end of file” warning.
  - Do not use slogans or colloquialisms. Replace `号令` with `一斉の施策` / `一斉導入`, etc., and replace `〜が効く` with `〜が有効である` / `〜を対象とする`, etc.
  - Do not use words that sound childish or immature. Replace `スローガン` with `方針` / `コンセプト`, etc. Avoid simplistic slogans and inflammatory language, and choose words appropriate for business documents.
- Reduce output bold makers and exclamation marks to maintain a professional tone.
- Instead of using `()`, arrow, or other symbols to indicate the flow of logic, use clear and concise language to describe the steps or processes involved.
- Do not use decorative characters. Specifically, bold text (`**`), arrows (`→` `←`), dashes (`—` `–`), `*`, and `=` used for definitions. Express emphasis and contrast in sentences. 
  - Exception: Only the tree symbol (`└─` `├─`) for directory structures and text diagrams is permitted.
- When indicating stages or flows, use words instead of arrows, such as "in the order of A, B, C" or "from A to B".
- Do not use prose, poetic, essayistic, or poetic expressions. Write facts and actions directly, rather than using metaphors or emotional paraphrases (e.g., "go with the flow of people," "a device called ~," "the backbone of the article").
- When using abstract words, immediately add a sentence of concrete paraphrasing (to prevent poeticism).
- Do not use parentheses () for paraphrasing or supplementary explanations in the main text. Incorporate the meaning of words into the sentence (e.g., `再現できる手順やプロンプト` instead of `再現できる形 (手順やプロンプト)`). References to facts, such as citations of sources, are acceptable.
- Avoid roundabout phrasing. State the conclusion directly and eliminate preambles and redundant paraphrasing.

## Workflow & Process
- **TDD (Test Driven Development):**
  - **Pre-requisite:** Do NOT generate implementation code immediately
  - **Phase 1 (Red):** Outline or write the failing test case first
    - In Plan mode, list test cases to add or modify in a table (Test Case Name, Input, Expected Result)
  - **Phase 2 (Green):** Write minimal code to satisfy the test
  - **Phase 3 (Refactor):** Optimize code structure
- **Verification:**
  - Always verify changes with available tests
  - If tests fail, analyze the root cause _before_ attempting a fix
- **Git**:
  - Follow conventional commit style: `<type>(<scope>): <description>`
  - Use `gh` command for any GitHub operations: such as getting PR details, issue info, creating PRs, etc.
  - When using `gh api`, always use GraphQL (`gh api graphql`) instead of REST endpoints
  - Write code comments in English
  - One commit per logical change
  - Create new reverting commit instead of rewriting history
  - Always specify origin and branch: `git push <origin> <branch>`
  - Run `git` directly when CWD is inside the repo; avoid `git -C <path>`.
- Grep:
  - Use `rg` (ripgrep) for searching codebase instead of `grep`

## Universal Safety Standards
- **Secrets:** NEVER output hardcoded API keys or passwords. Suggest environment variables.
- **Commands:** When suggesting shell commands, ensure they are non-destructive or include warnings.
  - Use `safe-rm` command instead of `rm` for deletions.

## Universal Coding Style
- **Naming:** Use clear, purpose-revealing variable names
- **Comments:**
  - Explain "Why" logic is complex, not "What" the code does.
  - Write only persistent information. Do not write time-dependent flow information (past PR numbers, closing history, chronological expressions like "last time..." or "this time...", list of ref links, references to options not adopted). Leave the history in the commit log or PR.
  - Do not write justifications or explanations for the writer's decisions. The responsibility for explaining "why the design decision I made is correct" and "why this method doesn't cause problems" lies with the commit message or PR body. Comments should only contain "facts necessary for the reader when encountering that code."
  - Do not paraphrase facts that can be gleaned from the code. Only write comments about parts that surprise, confuse, or cause errors in the reader.
  - Do not create explanatory blocks that group multiple facts; instead, distribute each fact as close as possible to the subject it explains (the part where the reader might have questions).
- In writing issue or pr description, you must write Japanese except user explicitly requests English. 

