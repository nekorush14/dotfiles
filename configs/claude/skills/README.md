# Claude Code Skills

このディレクトリには、ソフトウェア開発に特化したスキルが含まれており、単一責任の原則 (1 skill = 1 role) に従って整理されています。

## Supported Frameworks and Languages

- **Rails Development**: Ruby on Rails によるバックエンド開発
- **Python Development**: Core Python, FastAPI, pytest
- **TypeScript/React/Next.js Development**: TypeScript, React, Next.js によるフロントエンド開発
- **Shell Scripting**: Bash, Zsh, 汎用シェルスクリプト開発

## Table of Contents

- [Quick Reference](#quick-reference) ⭐
- [How to Choose a Skill](#how-to-choose-a-skill)
- [Directory Structure](#directory-structure)
- [Shared Resources](#shared-resources)
- [Getting Started](#getting-started)
- [Maintenance & Best Practices](#maintenance--best-practices)
- [History](#history)

---

## Quick Reference

### Rails Backend Skills

| Skill | Trigger Keywords | Use When |
|-------|-----------------|----------|
| `rails-service-objects` | service, business logic, multi-step | Business logic spanning multiple models |
| `rails-form-objects` | form, multi-model, validation | Multi-model form processing |
| `rails-model-design` | model, ActiveRecord, association | Model design and refactoring |
| `rails-transactions` | transaction, atomicity, consistency | Transaction management |
| `rails-query-optimization` | N+1, eager loading, performance | Query optimization |
| `rails-database-indexes` | index, query performance, migration | Index design |
| `rails-security` | authentication, authorization, security | Authentication, authorization, security |
| `rails-state-machines` | state, transition, workflow | State transition implementation |
| `rails-background-jobs` | async, job, email, queue | Asynchronous task processing |
| `rails-error-handling` | error, exception, rescue | Error handling |
| `rails-grpc-implementation` | grpc, microservices, streaming | gRPC service implementation |

### RSpec Testing Skills

| Skill | Trigger Keywords | Use When |
|-------|-----------------|----------|
| `rspec-model-testing` | test model, model spec, validation | Testing models |
| `rspec-request-testing` | test API, request spec, endpoint | Testing API/controllers |
| `rspec-service-testing` | test service, service spec | Testing service objects |
| `rspec-job-testing` | test job, job spec, background | Testing background jobs |
| `rspec-grpc-testing` | test grpc, grpc spec | Testing gRPC services |

### Python Development Skills

| Skill | Trigger Keywords | Use When |
|-------|-----------------|----------|
| `python-core-development` | class, dataclass, type hints, async, exception | Class design, type safety, error handling, async |
| `python-api-development` | FastAPI, API, endpoint, Pydantic, validation | REST API implementation with FastAPI |
| `pytest-testing` | pytest, test, fixture, mock, parametrize | Unit and integration testing |
| `pytest-api-testing` | test API, TestClient, endpoint test | API endpoint testing |

### TypeScript/React Development Skills

| Skill | Trigger Keywords | Use When |
|-------|-----------------|----------|
| `typescript-core-development` | type, generic, utility type, type guard, Result pattern | Type-safe code design, generics, functional patterns |
| `react-component-development` | component, hooks, useState, useEffect, custom hook | React component design and implementation |
| `react-state-management` | context, state, TanStack Query, server state | Global state, server state, optimistic updates |
| `react-styling` | Tailwind, CSS Modules, styled-components, styling | Component styling, responsive design, dark mode |

### Next.js Development Skills

| Skill | Trigger Keywords | Use When |
|-------|-----------------|----------|
| `nextjs-app-development` | app router, server component, server action, pages router | Next.js application development (App Router & Pages Router) |
| `nextjs-optimization` | image, font, performance, SEO, bundle, Core Web Vitals | Performance optimization, SEO improvements |

### Frontend Testing Skills

| Skill | Trigger Keywords | Use When |
|-------|-----------------|----------|
| `vitest-react-testing` | vitest, test component, react testing library, msw | Unit tests, component tests, API mocking |
| `playwright-testing` | e2e, playwright, page object, integration test | E2E tests, user flows, integration tests |
| `storybook-development` | storybook, story, component documentation | Component documentation, UI catalog, visual testing |

### Skill Creation Skills

| Skill | Trigger Keywords | Use When |
|-------|-----------------|----------|
| `skill-creator` | create skill, new skill, skill creation, skill structure | Creating new Agent Skills or updating existing skills |

### Shell Scripting Skills

| Skill | Trigger Keywords | Use When |
|-------|-----------------|----------|
| `shell-scripting` | bash, zsh, shell script, error handling, argument parsing, security | Writing/debugging shell scripts, implementing CLI tools |

---

## How to Choose a Skill

### Rails Development

```
Need to implement business logic?
├─ Single model → rails-model-design
├─ Multiple models → rails-service-objects
└─ Complex forms → rails-form-objects

Need data management?
├─ Transactions → rails-transactions
├─ Query optimization → rails-query-optimization
└─ Index design → rails-database-indexes

Need application features?
├─ Authentication/Authorization → rails-security
├─ State transitions → rails-state-machines
├─ Asynchronous processing → rails-background-jobs
├─ gRPC services → rails-grpc-implementation
└─ Error handling → rails-error-handling

Need to write tests?
├─ Model tests → rspec-model-testing
├─ API tests → rspec-request-testing
├─ Service tests → rspec-service-testing
├─ Job tests → rspec-job-testing
└─ gRPC tests → rspec-grpc-testing
```

### Python Development

```
Need to implement Python code?
├─ Class design / Type safety → python-core-development
├─ Error handling / Exceptions → python-core-development
├─ Async programming → python-core-development
└─ REST API endpoints → python-api-development

Need data validation?
├─ API request/response → python-api-development (Pydantic)
└─ Internal data → python-core-development (dataclass)

Need to write tests?
├─ Unit / Integration tests → pytest-testing
└─ API endpoint tests → pytest-api-testing

Need authentication?
└─ FastAPI auth → python-api-development
```

### TypeScript/React/Next.js Development

```
Need to implement TypeScript/React/Next.js code?
├─ Type definitions / Type safety → typescript-core-development
├─ React components / hooks → react-component-development
├─ Global state / Context API → react-state-management
├─ Server state / TanStack Query → react-state-management
├─ Component styling → react-styling
├─ Next.js pages / routes → nextjs-app-development
└─ Performance / SEO optimization → nextjs-optimization

Need to write tests?
├─ Unit / Component tests → vitest-react-testing
├─ E2E / User flow tests → playwright-testing
└─ Component documentation → storybook-development

Need styling?
├─ Tailwind CSS → react-styling
├─ CSS Modules → react-styling
└─ styled-components → react-styling
```

### Skill Creation

```
Need to create or update Agent Skills?
├─ Create new skill → skill-creator
├─ Update existing skill → skill-creator
├─ Validate skill format → skill-creator
└─ Learn best practices → skill-creator
```

### Shell Scripting

```
Need to write or debug shell scripts?
├─ Bash scripts → shell-scripting
├─ Zsh scripts → shell-scripting
├─ Error handling → shell-scripting
├─ Argument parsing → shell-scripting
├─ Security improvements → shell-scripting
└─ Cross-platform compatibility → shell-scripting
```

---

## Directory Structure

```
configs/claude/skills/
├── README.md                              # This file (skill catalog)
├── HISTORY.md                             # Migration history and archived skills
├── _shared/                               # Shared resources
│   ├── rails-coding-standards.md
│   ├── rails-tdd-workflow.md
│   ├── rspec-testing-fundamentals.md
│   ├── factory-bot-guide.md
│   ├── python-coding-standards.md
│   ├── python-tdd-workflow.md
│   ├── pytest-fundamentals.md
│   ├── typescript-coding-standards.md
│   ├── react-coding-standards.md
│   ├── vitest-fundamentals.md
│   └── frontend-tdd-workflow.md
├── rails-service-objects/                 # Rails skills
│   └── SKILL.md
├── python-core-development/               # Python skills
│   └── SKILL.md
├── typescript-core-development/           # TypeScript skills
│   └── SKILL.md
├── react-component-development/           # React skills
│   └── SKILL.md
├── nextjs-app-development/                # Next.js skills
│   └── SKILL.md
├── vitest-react-testing/                  # Testing skills
│   └── SKILL.md
├── skill-creator/                         # Skill creation
│   └── SKILL.md
└── shell-scripting/                       # Shell scripting
    ├── SKILL.md
    └── references/                        # Detailed documentation
        ├── bash-features.md
        ├── zsh-features.md
        ├── security-best-practices.md
        └── common-patterns.md
```

---

## Shared Resources

`_shared/` ディレクトリには、すべてのスキルから参照される共通の標準とワークフローが含まれています。

### Rails Standards

- **rails-coding-standards.md**: コーディング規約、インデント、リンティングルール
- **rails-tdd-workflow.md**: Test-Driven Development ワークフロー

### RSpec Testing

- **rspec-testing-fundamentals.md**: RSpec 構造、マッチャー、モッキング、ベストプラクティス
- **factory-bot-guide.md**: FactoryBot ファクトリ定義と使用パターン

### Python Standards

- **python-coding-standards.md**: PEP8, type hints, ruff/black/isort/flake8/mypy, docstrings
- **python-tdd-workflow.md**: pytest による Test-Driven Development ワークフロー

### Pytest Testing

- **pytest-fundamentals.md**: Pytest 構造、fixtures, parametrize, モッキングベストプラクティス

### TypeScript/React Standards

- **typescript-coding-standards.md**: ESLint/Prettier, 命名規則, import 順序, type ベストプラクティス
- **react-coding-standards.md**: Component 構造, Props パターン, Hooks ルール, ディレクトリ構造, パフォーマンスベストプラクティス

### Frontend Testing

- **vitest-fundamentals.md**: Vitest 構造、マッチャー、モック、React Testing Library 基礎、userEvent、async テスト
- **frontend-tdd-workflow.md**: TDD ワークフロー、テストコマンド、カバレッジ、リンティング、型チェック

---

## Getting Started

### Skill Selection

Claude Code は以下に基づいて適切なスキルを自動選択します：

- `description` フィールドのタスク説明
- "When to Use This Skill" セクションの起動トリガー
- ユーザーリクエストからのコンテキスト

### Skill Dependencies

スキルは "Related Skills" セクションを通じて相互参照します：

- `rails-service-objects` は `rails-transactions` をよく使用
- `rails-model-design` は `rails-database-indexes` と組み合わせて使用
- すべてのスキルは堅牢なエラー管理のために `rails-error-handling` を使用

### Testing

すべての実装スキルは TDD ワークフローに従います。

**Rails Testing (RSpec)**:

- `rspec-model-testing`: モデルスペック用
- `rspec-request-testing`: リクエスト/API スペック用
- `rspec-service-testing`: サービスオブジェクトスペック用
- `rspec-job-testing`: バックグラウンドジョブスペック用
- `rspec-grpc-testing`: gRPC サービススペック用

**Python Testing (Pytest)**:

- `pytest-testing`: ユニットテストと統合テスト用
- `pytest-api-testing`: API エンドポイントテスト用

**Frontend Testing (Vitest/Playwright)**:

- `vitest-react-testing`: ユニットテストとコンポーネントテスト用
- `playwright-testing`: E2E テスト用
- `storybook-development`: コンポーネントドキュメントとビジュアルテスト用

---

## Maintenance & Best Practices

### Adding New Skills

1. `configs/claude/skills/` 配下にディレクトリを作成
2. YAML frontmatter 付きの `SKILL.md` を追加
3. 構造に従う: name, description, when to use, principles, guidelines, tools, workflow
4. `_shared/` から共有標準を参照
5. この README に追加

### Updating Skills

- スキルを単一責任に保つ
- スキルあたり 80-500行を目安とする
- 変更時には関連スキルも更新
- 関連プロンプトでスキルの起動をテスト

### Best Practices

- **Single Responsibility**: 各スキルは1つの役割/機能を処理
- **Clear Triggers**: description に具体的な起動条件を記載
- **Concrete Examples**: 常にコード例を含める
- **Tool References**: 使用するツールを明示
- **Cross-References**: 関連スキルへのリンク
- **Shared Standards**: `_shared/` から共通標準を参照

### Code Quality

- すべてのスキルは TDD アプローチに従う
- 実装前にテストを作成
- 適切なエラーハンドリングを実装
- セキュリティベストプラクティスに従う

---

## History

スキルの進化の歴史、移行情報、アーカイブされたスキルについては [HISTORY.md](./HISTORY.md) を参照してください。

主なマイルストーン：

- モノリシック `rails-backend-dev` (300+ 行) → 10個の専門 Rails スキル
- モノリシック `rspec-test` (718行) → 4個の専門 RSpec スキル
- Python, TypeScript/React, Next.js, Shell Scripting スキルの追加 (2025)
- Skill Creator スキルの追加 (2025)
