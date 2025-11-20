# Claude Code Skills

This directory contains specialized skills for software development, organized by single responsibility principle (1 skill = 1 role).

Supported frameworks and languages:
- **Rails Development**: Backend development with Ruby on Rails
- **Python Development**: Core Python, FastAPI, and pytest
- **TypeScript/React/Next.js Development**: Frontend development with TypeScript, React, and Next.js

## Directory Structure

```
configs/claude/skills/
├── README.md                              # This file (skill catalog and guide)
├── _shared/                               # Shared resources (referenced by all skills)
│   ├── rails-coding-standards.md         # Rails coding conventions
│   ├── rails-tdd-workflow.md             # Rails TDD workflow
│   ├── rspec-testing-fundamentals.md     # RSpec fundamentals
│   ├── factory-bot-guide.md              # FactoryBot guide
│   ├── python-coding-standards.md        # Python coding conventions
│   ├── python-tdd-workflow.md            # Python TDD workflow
│   ├── pytest-fundamentals.md            # Pytest fundamentals
│   ├── typescript-coding-standards.md    # TypeScript coding conventions
│   ├── react-coding-standards.md         # React coding standards
│   ├── vitest-fundamentals.md            # Vitest fundamentals
│   └── frontend-tdd-workflow.md          # Frontend TDD workflow
├── rails-service-objects/                 # Rails skill
│   └── SKILL.md                          # Skill definition (YAML frontmatter required)
├── python-core-development/               # Python skill
│   └── SKILL.md
├── typescript-core-development/           # TypeScript skill
│   └── SKILL.md
├── react-component-development/           # React skill
│   └── SKILL.md
├── nextjs-app-development/                # Next.js skill
│   └── SKILL.md
├── vitest-react-testing/                  # Testing skill
│   └── SKILL.md
└── storybook-development/                 # Documentation skill
    └── SKILL.md
```

## Quick Reference

### Rails Backend Skills

| Skill | Trigger Keywords | Lines | Use When |
|-------|-----------------|-------|----------|
| `rails-service-objects` | service, business logic, multi-step | 169 | Business logic spanning multiple models |
| `rails-form-objects` | form, multi-model, validation | 192 | Multi-model form processing |
| `rails-model-design` | model, ActiveRecord, association | 241 | Model design and refactoring |
| `rails-transactions` | transaction, atomicity, consistency | 181 | Transaction management |
| `rails-query-optimization` | N+1, eager loading, performance | 225 | Query optimization |
| `rails-database-indexes` | index, query performance, migration | 262 | Index design |
| `rails-security` | authentication, authorization, security | 325 | Authentication, authorization, security |
| `rails-state-machines` | state, transition, workflow | 350 | State transition implementation |
| `rails-background-jobs` | async, job, email, queue | 350 | Asynchronous task processing |
| `rails-error-handling` | error, exception, rescue | 370 | Error handling |

### RSpec Testing Skills

| Skill | Trigger Keywords | Lines | Use When |
|-------|-----------------|-------|----------|
| `rspec-model-testing` | test model, model spec, validation | 236 | Testing models |
| `rspec-request-testing` | test API, request spec, endpoint | 220 | Testing API/controllers |
| `rspec-service-testing` | test service, service spec | 214 | Testing service objects |
| `rspec-job-testing` | test job, job spec, background | 234 | Testing background jobs |

### Python Development Skills

| Skill | Trigger Keywords | Lines | Use When |
|-------|-----------------|-------|----------|
| `python-core-development` | class, dataclass, type hints, async, exception | 320 | Class design, type safety, error handling, async |
| `python-api-development` | FastAPI, API, endpoint, Pydantic, validation | 280 | REST API implementation with FastAPI |
| `pytest-testing` | pytest, test, fixture, mock, parametrize | 330 | Unit and integration testing |
| `pytest-api-testing` | test API, TestClient, endpoint test | 300 | API endpoint testing |

### TypeScript/React Development Skills

| Skill | Trigger Keywords | Lines | Use When |
|-------|-----------------|-------|----------|
| `typescript-core-development` | type, generic, utility type, type guard, Result pattern | 330 | Type-safe code design, generics, functional patterns |
| `react-component-development` | component, hooks, useState, useEffect, custom hook | 400 | React component design and implementation |
| `react-state-management` | context, state, TanStack Query, server state | 345 | Global state, server state, optimistic updates |
| `react-styling` | Tailwind, CSS Modules, styled-components, styling | 350 | Component styling, responsive design, dark mode |

### Next.js Development Skills

| Skill | Trigger Keywords | Lines | Use When |
|-------|-----------------|-------|----------|
| `nextjs-app-development` | app router, server component, server action, pages router | 500 | Next.js application development (App Router & Pages Router) |
| `nextjs-optimization` | image, font, performance, SEO, bundle, Core Web Vitals | 315 | Performance optimization, SEO improvements |

### Frontend Testing Skills

| Skill | Trigger Keywords | Lines | Use When |
|-------|-----------------|-------|----------|
| `vitest-react-testing` | vitest, test component, react testing library, msw | 440 | Unit tests, component tests, API mocking |
| `playwright-testing` | e2e, playwright, page object, integration test | 355 | E2E tests, user flows, integration tests |
| `storybook-development` | storybook, story, component documentation | 315 | Component documentation, UI catalog, visual testing |

### Skill Creation Skills

| Skill | Trigger Keywords | Lines | Use When |
|-------|-----------------|-------|----------|
| `skill-creator` | create skill, new skill, skill creation, skill structure | 480 | Creating new Agent Skills or updating existing skills |

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
└─ Error handling → rails-error-handling

Need to write tests?
├─ Model tests → rspec-model-testing
├─ API tests → rspec-request-testing
├─ Service tests → rspec-service-testing
└─ Job tests → rspec-job-testing
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

## Shared Resources

### `_shared/`

Common standards and workflows referenced by all skills:

#### Rails Standards

- **rails-coding-standards.md**: Coding conventions, indentation, linting rules
- **rails-tdd-workflow.md**: Test-Driven Development workflow

#### RSpec Testing

- **rspec-testing-fundamentals.md**: RSpec structure, matchers, mocking, and best practices
- **factory-bot-guide.md**: FactoryBot factory definitions and usage patterns

#### Python Standards

- **python-coding-standards.md**: PEP8, type hints, ruff/black/isort/flake8/mypy, docstrings
- **python-tdd-workflow.md**: Test-Driven Development workflow with pytest

#### Pytest Testing

- **pytest-fundamentals.md**: Pytest structure, fixtures, parametrize, mocking best practices

#### TypeScript/React Standards

- **typescript-coding-standards.md**: ESLint/Prettier, naming conventions, import order, type best practices
- **react-coding-standards.md**: Component structure, Props patterns, Hooks rules, directory structure, performance best practices

#### Frontend Testing

- **vitest-fundamentals.md**: Vitest structure, matchers, mocks, React Testing Library basics, userEvent, async testing
- **frontend-tdd-workflow.md**: TDD workflow, test commands, coverage, linting, type checking

## Rails Backend Skills

### Core Development

#### `rails-service-objects/`

**Role**: Service object design and implementation

- Multi-step business workflows
- Transaction coordination
- Result object pattern
- **Use when**: Business logic spans multiple models or requires complex coordination

#### `rails-form-objects/`

**Role**: Form object implementation

- Multi-model forms
- Complex validations
- Virtual attributes
- **Use when**: Forms involve multiple models or complex validation logic

#### `rails-model-design/`

**Role**: ActiveRecord model design

- Model associations
- Validations and scopes
- Domain methods
- **Use when**: Creating or refactoring models

### Data Management

#### `rails-transactions/`

**Role**: Database transaction management

- Atomic operations
- Data consistency
- Transaction isolation
- **Use when**: Operations must succeed or fail together

#### `rails-query-optimization/`

**Role**: Query performance optimization

- N+1 query prevention
- Eager loading strategies
- Query analysis
- **Use when**: Optimizing slow queries or preventing N+1 issues

#### `rails-database-indexes/`

**Role**: Database index design

- Index creation
- Composite indexes
- Performance optimization
- **Use when**: Creating tables or optimizing query performance

### Application Features

#### `rails-security/`

**Role**: Security implementation

- Authentication & authorization
- Protection against vulnerabilities
- Strong parameters
- **Use when**: Implementing user access control or securing endpoints

#### `rails-state-machines/`

**Role**: State machine implementation (AASM)

- State transitions
- Workflow management
- Event-driven logic
- **Use when**: Models have distinct states with defined transitions

#### `rails-background-jobs/`

**Role**: Asynchronous job processing

- Background task execution
- Email delivery
- Job queues and scheduling
- **Use when**: Tasks should run asynchronously (emails, reports, imports)

#### `rails-error-handling/`

**Role**: Error handling and recovery

- Exception handling
- Error responses
- Logging strategies
- **Use when**: Implementing robust error handling or recovery logic

## RSpec Testing Skills

### `rspec-model-testing/`

**Role**: Model spec writing

- Testing validations and associations
- Testing scopes and methods
- Testing callbacks
- **Use when**: Writing tests for ActiveRecord models

### `rspec-request-testing/`

**Role**: Request/API spec writing

- Testing API endpoints
- Testing HTTP responses
- Testing authentication
- **Use when**: Writing tests for controllers or API endpoints

### `rspec-service-testing/`

**Role**: Service object spec writing

- Testing business logic
- Testing transactions
- Testing error handling
- **Use when**: Writing tests for service objects or form objects

### `rspec-job-testing/`

**Role**: Background job spec writing

- Testing job execution
- Testing retry logic
- Testing job enqueuing
- **Use when**: Writing tests for ActiveJob background jobs

## TypeScript/React/Next.js Skills

### Core Development

#### `typescript-core-development/`

**Role**: Type-safe TypeScript code design

- Type system and generics
- Utility types and type guards
- Functional programming patterns
- Result/Either pattern for errors
- **Use when**: Designing type-safe code, implementing generics, handling errors

#### `react-component-development/`

**Role**: React component design and implementation

- Functional components with hooks
- Custom hooks implementation
- Component composition patterns
- Performance optimization
- **Use when**: Creating React components, implementing custom hooks, optimizing performance

#### `react-state-management/`

**Role**: Application state management

- Context API patterns
- TanStack Query for server state
- State selection guidelines
- Optimistic updates
- **Use when**: Managing global state, handling server state, implementing optimistic updates

#### `react-styling/`

**Role**: Component styling

- Tailwind CSS utility classes
- CSS Modules patterns
- CSS-in-JS (styled-components/Emotion)
- Responsive design and dark mode
- **Use when**: Styling components, implementing responsive design, creating design systems

### Next.js Development

#### `nextjs-app-development/`

**Role**: Next.js application development

- App Router (Server Components, Server Actions)
- Pages Router (getServerSideProps, getStaticProps)
- Data fetching strategies
- Route Handlers and API Routes
- **Use when**: Building Next.js applications, implementing SSR/SSG, creating API routes

#### `nextjs-optimization/`

**Role**: Performance and SEO optimization

- Image and font optimization
- Bundle optimization and code splitting
- Caching strategies
- SEO metadata and sitemaps
- Core Web Vitals improvements
- **Use when**: Optimizing performance, improving SEO, enhancing user experience

### Testing

#### `vitest-react-testing/`

**Role**: Unit and component testing

- Vitest unit tests
- React Testing Library component tests
- MSW for API mocking
- Custom hook testing
- **Use when**: Writing unit tests, testing components, mocking APIs

#### `playwright-testing/`

**Role**: E2E testing with Playwright

- E2E test implementation
- Page Object Model
- Visual regression testing
- CI/CD integration
- **Use when**: Testing user flows, E2E testing, visual testing

#### `storybook-development/`

**Role**: Component documentation and testing

- Story creation (CSF3)
- Interaction testing
- Visual regression testing
- Component catalog
- **Use when**: Documenting components, creating UI catalog, visual testing

## Python Development Skills

### Core Development

#### `python-core-development/`

**Role**: Core Python development with type safety and best practices

- Dataclass and Protocol patterns
- Type hints and type safety
- Custom exceptions and error handling
- Async/await programming
- Context managers
- **Use when**: Designing classes, implementing type safety, error handling, or async code

#### `python-api-development/`

**Role**: REST API development with FastAPI

- FastAPI endpoint implementation
- Pydantic models for validation
- Dependency injection
- Authentication and authorization
- Structured error responses
- **Use when**: Building REST API endpoints with FastAPI

### Testing

#### `pytest-testing/`

**Role**: Unit and integration testing with pytest

- Pytest test structure and fixtures
- Mocking with unittest.mock
- Parametrize for multiple scenarios
- Async test support
- **Use when**: Writing unit or integration tests for Python code

#### `pytest-api-testing/`

**Role**: API endpoint testing with TestClient

- FastAPI TestClient patterns
- Request/response validation
- Authentication testing
- Error response testing
- Integration testing
- **Use when**: Writing tests for FastAPI endpoints

## Skill Creation Skills

### `skill-creator/`

**Role**: Creating effective Agent Skills

- Skill initialization and structure
- YAML frontmatter validation
- Progressive disclosure patterns
- Best practices and conventions
- Skill validation and testing
- **Use when**: Creating new skills, updating existing skills, or learning skill authoring best practices

## Archived Skills

### `_archived/rails-backend-dev/`

Original monolithic skill (300+ lines) that has been refactored into 10 specialized Rails backend skills.

### `_archived/rspec-test/`

Original monolithic testing skill (718 lines) that has been refactored into 4 specialized RSpec testing skills.

## Usage Guidelines

### Skill Selection

Claude Code automatically selects appropriate skills based on:

- Task description in the `description` field
- Activation triggers in "When to Use This Skill" section
- Context from user requests

### Skill Dependencies

Skills reference each other through "Related Skills" sections:

- `rails-service-objects` often uses `rails-transactions`
- `rails-model-design` benefits from `rails-database-indexes`
- All skills use `rails-error-handling` for robust error management

### Testing

All implementation skills follow TDD workflow.

**Rails Testing (RSpec):**
- `rspec-model-testing`: For model specs
- `rspec-request-testing`: For request/API specs
- `rspec-service-testing`: For service object specs
- `rspec-job-testing`: For background job specs

**Python Testing (Pytest):**
- `pytest-testing`: For unit and integration tests
- `pytest-api-testing`: For API endpoint tests

## Maintenance

### Adding New Skills

1. Create directory under `configs/claude/skills/`
2. Add `SKILL.md` with YAML frontmatter
3. Follow structure: name, description, when to use, principles, guidelines, tools, workflow
4. Reference shared standards from `_shared/`
5. Add to this README

### Updating Skills

- Keep skills focused on single responsibility
- Aim for 80-150 lines per skill
- Update related skills when making changes
- Test skill activation with relevant prompts

## Best Practices

- **Single Responsibility**: Each skill handles one role/capability
- **Clear Triggers**: Specific activation conditions in description
- **Concrete Examples**: Always include code examples
- **Tool References**: Specify which tools to use
- **Cross-References**: Link to related skills
- **Shared Standards**: Reference common standards from `_shared/`

## Migration History

### From rails-backend-dev (300+ lines → 10 skills)

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

| Original Section | New Skill/Resource | Lines |
|-----------------|-------------------|-------|
| Model Specs | `rspec-model-testing` | 236 |
| Request Specs | `rspec-request-testing` | 220 |
| Service Specs | `rspec-service-testing` | 214 |
| Job Specs | `rspec-job-testing` | 234 |
| RSpec Fundamentals | `_shared/rspec-testing-fundamentals.md` | 165 |
| FactoryBot | `_shared/factory-bot-guide.md` | 173 |

### Python Skills (New in 2025)

| Skill | Category | Lines |
|-------|----------|-------|
| `python-core-development` | Core Development | 320 |
| `python-api-development` | API Development | 280 |
| `pytest-testing` | Testing | 330 |
| `pytest-api-testing` | API Testing | 300 |
| `_shared/python-coding-standards.md` | Shared Resource | 140 |
| `_shared/python-tdd-workflow.md` | Shared Resource | 70 |
| `_shared/pytest-fundamentals.md` | Shared Resource | 250 |

### Benefits

Each skill is now:

- **Focused**: Single responsibility per skill
- **Appropriately Sized**: 165-370 lines (Rails), 280-330 lines (Python)
- **Independently Maintainable**: Changes isolated to specific skills
- **Easier to Select**: Claude can choose the right skill more accurately
- **Reusable**: Shared resources reduce duplication
- **Multi-Language**: Support for both Rails and Python development
