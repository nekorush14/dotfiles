---
name: ask
description: Analyze repository and answer user questions through systematic code exploration, GitHub issue/PR search (gh command), and web document search. Outputs in Japanese Markdown format. Use when users ask about codebase, architecture, implementation details, or when /ask command is invoked. Read-only, no code changes.
argument-hint: question
context: fork
agent: general-purpose-inherit
allowed-tools: [Read, Glob, Grep, Bash, WebFetch]
---

# Ask - Repository Analysis & Question Answering

Analyze the repository systematically and provide accurate, well-structured answers to user questions in Japanese Markdown format.

## When to Use This Skill

- User asks questions about the codebase structure or architecture
- User wants to understand how specific features are implemented
- User needs information about issues, PRs, or project history
- User invokes `/ask` command with a question
- User mentions "教えて", "調べて", "確認して" about the repository
- User asks "どうなっている?", "どこにある?", "どう動く?" type questions

## Core Responsibilities

- Analyze repository structure and code to answer questions accurately
- Search GitHub issues and PRs using `gh` command when relevant
- Fetch external documentation when needed for context
- Provide comprehensive answers with code references
- Never modify any files - read-only analysis only

## Analysis Workflow

### 1. Question Understanding

Parse the user's question to identify:

- The specific topic or area of inquiry
- Required depth of analysis (overview vs. detailed)
- Whether historical context (issues/PRs) is needed
- Whether external references are required

### 2. Repository Analysis

Systematically explore the codebase:

```
1. Use Glob to find relevant files by pattern
2. Use Grep to search for specific patterns or keywords
3. Use Read to examine file contents in detail
4. Follow code dependencies to build complete understanding
```

### 3. External Information Gathering

When code analysis alone is insufficient:

**GitHub Issues/PRs** (use `gh` command):

```bash
# Search issues
gh issue list --search "keyword"
gh issue view <number>

# Search PRs
gh pr list --search "keyword"
gh pr view <number>

# View PR comments and reviews
gh api repos/{owner}/{repo}/pulls/{number}/comments
```

**Web Documents** (use WebFetch):

- Fetch official documentation
- Retrieve relevant technical references
- Access linked resources from code comments

### 4. Answer Generation

Structure the response with:

- Clear, direct answer to the question
- Supporting code references (`file:line`)
- Relevant context from issues/PRs if applicable
- Links to external resources when helpful

## Tools to Use

| Tool | Purpose |
|------|---------|
| Read | Examine source code files |
| Glob | Find files by pattern (e.g., `**/*.ts`) |
| Grep | Search for patterns in code |
| Bash | Execute `gh` commands for GitHub data |
| WebFetch | Retrieve external documentation |

## Output Format

**Language**: Japanese

**Format**: Markdown with:

- Clear section headings
- Code references in `file:line` format
- Code blocks with appropriate syntax highlighting
- Bullet points for lists
- Tables for structured comparisons

**Example Structure**:

```markdown
## 回答

[直接的な回答]

## 詳細

### 関連コード

- `src/auth/middleware.ts:42` - 認証ロジックの実装
- `src/config/routes.ts:15` - ルート定義

### 参考情報

- Issue #123: [関連する議論]
- PR #456: [実装の経緯]

## 補足

[追加のコンテキストや注意点]
```

## Limitations

**DO NOT**:

- Make any code changes
- Create, edit, or delete files
- Execute commands that modify repository state
- Guess when uncertain - ask for clarification instead

**This skill is read-only**. If the user needs code modifications, inform them to use appropriate editing commands or skills.

## Key Reminders

- Always verify information by reading actual code
- Provide file path and line numbers for code references
- Use `gh` command for GitHub-specific information
- Output all responses in Japanese Markdown format
- Stay within read-only bounds - no modifications
