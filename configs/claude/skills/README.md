# Claude Code Skills for Rails Development

This directory contains specialized skills for Rails development, organized by single responsibility principle (1 skill = 1 role).

## Directory Structure

```
configs/claude/skills/
├── README.md                              # This file (skill catalog and guide)
├── _shared/                               # Shared resources (referenced by all skills)
│   ├── rails-coding-standards.md         # Coding conventions
│   ├── rails-tdd-workflow.md             # TDD workflow
│   ├── rspec-testing-fundamentals.md     # RSpec fundamentals
│   └── factory-bot-guide.md              # FactoryBot guide
├── rails-service-objects/                 # Individual skill
│   └── SKILL.md                          # Skill definition (YAML frontmatter required)
├── rails-model-design/
│   └── SKILL.md
└── rspec-model-testing/
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

## How to Choose a Skill

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

## Shared Resources

### `_shared/`

Common standards and workflows referenced by all skills:

#### Rails Standards

- **rails-coding-standards.md**: Coding conventions, indentation, linting rules
- **rails-tdd-workflow.md**: Test-Driven Development workflow

#### RSpec Testing

- **rspec-testing-fundamentals.md**: RSpec structure, matchers, mocking, and best practices
- **factory-bot-guide.md**: FactoryBot factory definitions and usage patterns

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

All Rails implementation skills follow TDD workflow. Use RSpec testing skills for writing tests:

- `rspec-model-testing`: For model specs
- `rspec-request-testing`: For request/API specs
- `rspec-service-testing`: For service object specs
- `rspec-job-testing`: For background job specs

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

### Benefits

Each skill is now:

- **Focused**: Single responsibility per skill
- **Appropriately Sized**: 165-370 lines (vs 300-718 original)
- **Independently Maintainable**: Changes isolated to specific skills
- **Easier to Select**: Claude can choose the right skill more accurately
- **Reusable**: Shared resources reduce duplication
