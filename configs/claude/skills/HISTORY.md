# Claude Code Skills - History

このファイルには、Skills の進化の歴史と移行情報を記録しています。

## Migration History

### From rails-backend-dev (300+ lines → 10 skills)

元のモノリシックな `rails-backend-dev` スキル (300+ 行) を、単一責任の原則に従って10個の専門スキルにリファクタリングしました。

| Original Section | New Skill | Lines |
|-----------------|-----------|-------|
| Service Objects | `rails-service-objects` | 169 |
| Form Objects | `rails-form-objects` | 192 |
| ActiveRecord Models | `rails-model-design` | 241 |
| Transaction Management | `rails-transactions` | 181 |
| N+1 Prevention | `rails-query-optimization` | 225 |
| Database Indexes | `rails-database-indexes` | 262 |
| Security | `rails-security` | 325 |
| State Machines | `rails-state-machines` | 350 |
| Background Jobs | `rails-background-jobs` | 350 |
| Error Handling | `rails-error-handling` | 370 |

### From rspec-test (718 lines → 4 skills + 2 shared resources)

元のモノリシックな `rspec-test` スキル (718行) を、4つの専門スキルと2つの共有リソースに分割しました。

| Original Section | New Skill/Resource | Lines |
|-----------------|-------------------|-------|
| Model Specs | `rspec-model-testing` | 236 |
| Request Specs | `rspec-request-testing` | 220 |
| Service Specs | `rspec-service-testing` | 214 |
| Job Specs | `rspec-job-testing` | 234 |
| RSpec Fundamentals | `_shared/rspec-testing-fundamentals.md` | 165 |
| FactoryBot | `_shared/factory-bot-guide.md` | 173 |

### Python Skills (New in 2025)

Python 開発サポートのために新規作成されたスキルです。

| Skill | Category | Lines |
|-------|----------|-------|
| `python-core-development` | Core Development | 320 |
| `python-api-development` | API Development | 280 |
| `pytest-testing` | Testing | 330 |
| `pytest-api-testing` | API Testing | 300 |
| `_shared/python-coding-standards.md` | Shared Resource | 140 |
| `_shared/python-tdd-workflow.md` | Shared Resource | 70 |
| `_shared/pytest-fundamentals.md` | Shared Resource | 250 |

### TypeScript/React/Next.js Skills (New in 2025)

フロントエンド開発サポートのために新規作成されたスキルです。

| Skill | Category | Lines |
|-------|----------|-------|
| `typescript-core-development` | Core Development | 330 |
| `react-component-development` | React Development | 400 |
| `react-state-management` | State Management | 345 |
| `react-styling` | Styling | 350 |
| `nextjs-app-development` | Next.js Development | 500 |
| `nextjs-optimization` | Optimization | 315 |
| `vitest-react-testing` | Testing | 440 |
| `playwright-testing` | E2E Testing | 355 |
| `storybook-development` | Documentation | 315 |
| `_shared/typescript-coding-standards.md` | Shared Resource | 180 |
| `_shared/react-coding-standards.md` | Shared Resource | 200 |
| `_shared/vitest-fundamentals.md` | Shared Resource | 180 |
| `_shared/frontend-tdd-workflow.md` | Shared Resource | 80 |

### Shell Scripting Skills (New in 2025)

シェルスクリプト開発サポートのために新規作成されたスキルです。

| Skill/Resource | Category | Lines |
|----------------|----------|-------|
| `shell-scripting` | Core Development | 432 |
| `references/bash-features.md` | Reference | 450+ |
| `references/zsh-features.md` | Reference | 400+ |
| `references/security-best-practices.md` | Reference | 650+ |
| `references/common-patterns.md` | Reference | 800+ |

### Skill Creation Skills (New in 2025)

Agent Skill の作成をサポートするために新規作成されたスキルです。

| Skill | Lines |
|-------|-------|
| `skill-creator` | 480 |

## Benefits of Migration

各スキルは以下の特徴を持つようになりました：

- **Focused**: 単一責任の原則に従った明確な役割
- **Appropriately Sized**: 適切なサイズ (165-500行)
- **Independently Maintainable**: 変更が特定のスキルに隔離される
- **Easier to Select**: Claude が適切なスキルをより正確に選択可能
- **Reusable**: 共有リソースによる重複の削減
- **Multi-Language**: Rails, Python, TypeScript/React, Shell scripting の包括的サポート

## Archived Skills

以下のスキルはアーカイブされています (機能する可能性はありますが、新しいモジュラーアプローチに置き換えられています)：

### `_archived/rails-backend-dev/`

オリジナルのモノリシックスキル (300+ 行) で、10個の専門 Rails backend スキルにリファクタリングされました。

### `_archived/rspec-test/`

オリジナルのモノリシックテストスキル (718行) で、4個の専門 RSpec テストスキルにリファクタリングされました。
