# Claude Code Agent Skills: Best Practices

Comprehensive guide for creating effective, maintainable Claude Code Agent Skills.

## Table of Contents

- [Core Principles](#core-principles)
- [Description Writing](#description-writing)
- [Progressive Disclosure](#progressive-disclosure)
- [Code Examples](#code-examples)
- [Tool Usage](#tool-usage)
- [Validation and Testing](#validation-and-testing)
- [Common Anti-Patterns](#common-anti-patterns)

## Core Principles

### Context Window is a Public Good

**Principle**: Only include information Claude doesn't already possess. Every token should justify its cost.

**Guidelines**:
- Don't explain basic language syntax (Claude already knows)
- Focus on domain-specific patterns and workflows
- Remove redundant explanations
- Use progressive disclosure for detailed content

**Example - Bad**:
```markdown
## Python Basics

Python uses indentation for code blocks. Variables are dynamically typed.
Functions are defined with the `def` keyword.
```

**Example - Good**:
```markdown
## Domain-Specific Pattern

Use Result[T, E] pattern for explicit error handling:

```python
from dataclasses import dataclass
from typing import Generic, TypeVar, Union

T = TypeVar('T')
E = TypeVar('E')

@dataclass
class Ok(Generic[T]):
    value: T

@dataclass
class Err(Generic[E]):
    error: E

Result = Union[Ok[T], Err[E]]
```
```

### Appropriate Freedom Level

**Principle**: Match specificity to task fragility.

| Freedom Level | When to Use | Format |
|--------------|-------------|---------|
| High | Flexible approaches acceptable | Text-based instructions |
| Medium | Patterns exist but variation OK | Pseudocode + examples |
| Low | Exact sequence required | Step-by-step commands |

**High Freedom Example**:
```markdown
## Implement Error Handling

Design custom exceptions that:
- Inherit from appropriate base classes
- Include contextual information
- Provide clear error messages
- Enable recovery strategies
```

**Low Freedom Example**:
```markdown
## Database Migration Steps

1. Create migration file:
   ```bash
   rails generate migration AddIndexToUsers email:index
   ```

2. Edit migration to specify index options:
   ```ruby
   add_index :users, :email, unique: true
   ```

3. Run migration:
   ```bash
   rails db:migrate
   ```

4. Verify in schema.rb:
   ```bash
   grep "add_index.*users.*email" db/schema.rb
   ```
```

### Model Testing

**Principle**: Test skills across Claude Haiku, Sonnet, and Opus.

Haiku may need more explicit instructions than Sonnet/Opus.

## Description Writing

### Anatomy of Good Description

**Format**: `[What it does]. Use when [trigger scenarios].`

**Components**:
1. **Functionality**: What the skill does (verbs)
2. **Trigger**: When to activate (scenarios)
3. **Scope**: What's included/excluded (optional)

### Examples

**Excellent**:
```yaml
description: Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDF files or when the user mentions PDFs.
```

Analysis:
- ✅ Clear functionality (extract, fill, merge)
- ✅ Explicit triggers (PDF files, user mentions PDFs)
- ✅ Specific scope (text, tables, forms)

**Good**:
```yaml
description: Implement Python code with dataclasses, type hints, protocols, error handling, and async programming. Use when designing classes, implementing type safety, handling exceptions, or writing async code.
```

Analysis:
- ✅ Lists specific features
- ✅ Multiple trigger scenarios
- ✅ Clear scope boundaries

**Bad**:
```yaml
description: Python development tool
```

Problems:
- ❌ Too vague
- ❌ No triggers
- ❌ Unclear scope

**Bad**:
```yaml
description: Helps with backend development tasks including APIs, databases, and services
```

Problems:
- ❌ Too broad
- ❌ Missing "Use when" clause
- ❌ Overly generic

### Trigger Keywords

Include specific trigger words that users might mention:

- Technical terms: "API", "database", "authentication"
- File types: "PDF", "Excel", "JSON"
- Operations: "deploy", "migrate", "refactor"
- Problems: "N+1 queries", "memory leak", "race condition"

## Progressive Disclosure

### Three-Level Architecture

**Level 1: Metadata** (Always Loaded)
- YAML frontmatter only
- `name` and `description`
- Claude reads to decide activation

**Level 2: Skill Body** (Loaded When Activated)
- SKILL.md content after frontmatter
- Overview and core principles (50-150 lines)
- Essential patterns with examples
- Tool usage and workflow
- Target: <500 lines total

**Level 3: References** (Loaded On Demand)
- Separate files in references/ directory
- Detailed API docs
- Extended examples
- Advanced patterns
- One level deep (no nested subdirectories)

### Structuring Large Skills

**Pattern 1: Domain-Based Split**

```
skill-name/
├── SKILL.md                 # Overview, core patterns
├── references/
│   ├── api-reference.md     # Complete API documentation
│   ├── examples.md          # Extended examples
│   └── advanced.md          # Advanced techniques
```

**Pattern 2: Feature-Based Split**

```
rails-api-development/
├── SKILL.md                 # Overview, basic patterns
├── references/
│   ├── authentication.md    # Auth patterns
│   ├── serialization.md     # JSON serialization
│   └── versioning.md        # API versioning
```

**Pattern 3: Workflow-Based Split**

```
deployment/
├── SKILL.md                 # Overview, basic deploy
├── references/
│   ├── environments.md      # Environment setup
│   ├── rollback.md          # Rollback procedures
│   └── monitoring.md        # Post-deploy monitoring
```

### Reference File Best Practices

**Always Include Table of Contents**:

```markdown
# API Reference

## Table of Contents

- [Authentication](#authentication)
- [Endpoints](#endpoints)
  - [Users API](#users-api)
  - [Products API](#products-api)
- [Error Handling](#error-handling)
```

**Use Descriptive Filenames**:
- ✅ `api-reference.md`, `error-handling.md`
- ❌ `docs.md`, `misc.md`, `other.md`

**Keep Files Focused**:
- One topic per file
- 200-400 lines per reference file
- Split if exceeding 500 lines

## Code Examples

### Essential Guidelines

**1. Include WHY Comments**

```python
# WHY: Use functional update when new state depends on previous state
setCount(prevCount => prevCount + 1)
```

**2. Make Examples Minimal**

Bad (too much context):
```python
# 50 lines of setup code
# ...
result = process_data(data)  # The actual example
```

Good (focused):
```python
# Minimal setup
data = {"user_id": 1, "action": "login"}

# WHY: Process ensures data validation before storage
result = process_data(data)
```

**3. Show Input/Output Pairs**

```python
# Input
user = User(email="invalid-email", name="John")

# Output: Raises ValidationError
# ValidationError: Invalid email format (field: email)
```

**4. Demonstrate Edge Cases**

```python
# Edge case: Empty list
result = process_items([])  # Returns empty result, no error

# Edge case: Single item
result = process_items([item])  # Processes without special handling

# Edge case: Duplicate items
result = process_items([item, item])  # WHY: Deduplicates automatically
```

### Example Structure

```markdown
### Pattern Name

Brief description of when to use this pattern.

```language
# WHY: Explain the key decision or tradeoff
code example showing the pattern
```

**Usage**:
```language
concrete example of using the pattern
```

**Avoid**:
```language
# What NOT to do
antipattern example
```
```

## Tool Usage

### Specify Allowed Tools

Restrict tools when skill has specific requirements:

```yaml
---
name: pdf-processing
description: Extract and manipulate PDF files
allowed-tools: [Read, Write, Bash, WebFetch]
---
```

**Why restrict**:
- Security: Prevent unintended file modifications
- Focus: Keep skill on task
- Performance: Reduce decision space

### Document Tool Patterns

```markdown
## Tools to Use

- `Read`: Read existing configuration files
- `Write`: Create new configuration files
- `Edit`: Modify configuration values
- `Bash`: Run configuration validation

### Common Commands

```bash
# Validate configuration
config-tool validate config.yaml

# Test configuration
config-tool test --dry-run config.yaml
```
```

## Validation and Testing

### Pre-Release Checklist

**YAML Frontmatter**:
- [ ] `name` is lowercase, hyphens, <64 chars
- [ ] `description` includes "Use when" clause
- [ ] `description` <1024 chars, no XML tags
- [ ] All fields are valid types

**Content**:
- [ ] SKILL.md <500 lines (move content to references/)
- [ ] Code examples include WHY comments
- [ ] Examples are minimal and focused
- [ ] Reference files have table of contents
- [ ] Forward slashes in all paths

**Testing**:
- [ ] Run validate_skill.py
- [ ] Test activation with trigger phrases
- [ ] Verify Claude discovers skill automatically
- [ ] Test with different models (Haiku, Sonnet, Opus)

### Validation Script Usage

```bash
# Validate skill
python validate_skill.py configs/claude/skills/my-skill

# Check output
✅ Name: my-skill
✅ Description: 256 chars
📊 File size: 8192 bytes, 245 lines
✅ Validation PASSED
```

### Activation Testing

Test phrases that should trigger your skill:

```markdown
# For python-core-development skill

Test phrases:
- "Design a Python class with type hints"
- "Implement error handling in Python"
- "Create a dataclass for user data"
- "Write async Python code"

All should activate the skill automatically.
```

## Common Anti-Patterns

### ❌ Information Overload

**Problem**: Including everything Claude already knows.

**Bad**:
```markdown
## Python Syntax

Python uses indentation. Variables don't need type declarations.
For loops iterate over sequences. The `def` keyword defines functions.
```

**Good**:
```markdown
## Domain Pattern: Result Type

Use Result type for explicit error handling in domain logic:
[specific example]
```

### ❌ Vague Triggers

**Problem**: Description doesn't specify when to activate.

**Bad**:
```yaml
description: Backend development tool
```

**Good**:
```yaml
description: Implement service objects for Rails multi-model business logic. Use when operations span multiple models, require transactions, or implement complex workflows.
```

### ❌ Monolithic Skills

**Problem**: One skill trying to do too much.

**Bad**:
```yaml
name: backend-development
description: Handle all backend tasks
```

**Good**:
```yaml
# Split into focused skills
name: rails-service-objects
name: rails-query-optimization
name: rails-security
```

### ❌ Missing Examples

**Problem**: Instructions without concrete code.

**Bad**:
```markdown
## Error Handling

Implement proper error handling with custom exceptions.
```

**Good**:
```markdown
## Error Handling

```python
class ValidationError(ApplicationError):
    def __init__(self, message: str, field: Optional[str] = None):
        super().__init__(message, code="VALIDATION_ERROR")
        self.field = field

# WHY: Raises early with field context for debugging
if not email or "@" not in email:
    raise ValidationError("Invalid email format", field="email")
```
```

### ❌ Unclear Workflows

**Problem**: No clear step-by-step process.

**Bad**:
```markdown
## Usage

Use this skill to handle API requests.
```

**Good**:
```markdown
## Workflow

1. **Define Endpoint**: Create route with HTTP method
2. **Validate Input**: Use Pydantic models for request validation
3. **Process Request**: Call service layer for business logic
4. **Handle Errors**: Catch exceptions and return error responses
5. **Return Response**: Serialize with response model
6. **Test**: Write tests for happy path and error cases
```

### ❌ Windows Paths

**Problem**: Using backslashes in paths.

**Bad**:
```python
path = "configs\\claude\\skills\\my-skill"
```

**Good**:
```python
path = "configs/claude/skills/my-skill"
```

### ❌ Nested References

**Problem**: References directory with subdirectories.

**Bad**:
```
references/
├── api/
│   ├── users.md
│   └── products.md
└── guides/
    └── deployment.md
```

**Good**:
```
references/
├── api-users.md
├── api-products.md
└── deployment-guide.md
```

## Iterative Improvement

### Development Workflow

1. **Create minimal viable skill**
   - Basic structure
   - Core patterns only
   - Essential examples

2. **Test with real scenarios**
   - Try trigger phrases
   - Use in actual projects
   - Observe Claude's behavior

3. **Collect feedback**
   - What worked well?
   - What was confusing?
   - What was missing?

4. **Refine incrementally**
   - Improve description for better activation
   - Add missing patterns
   - Move content to references if >500 lines
   - Update examples based on real usage

5. **Validate and test again**
   - Run validation script
   - Test activation triggers
   - Verify examples are still relevant

### Metrics to Track

- **Activation rate**: Is Claude finding your skill?
- **Completion rate**: Does Claude successfully complete tasks?
- **Token efficiency**: Are you using minimal tokens?
- **Error rate**: Are there common failure patterns?

## Summary

**Golden Rules**:

1. **Be Concise**: Context window is precious
2. **Be Specific**: Clear triggers in description
3. **Be Practical**: Concrete examples with WHY comments
4. **Be Focused**: One responsibility per skill
5. **Be Layered**: Use progressive disclosure
6. **Be Testable**: Validate and test thoroughly

**Quality Checklist**:

- [ ] Description includes "Use when" clause
- [ ] SKILL.md <500 lines
- [ ] Examples include WHY comments
- [ ] References have table of contents
- [ ] Validation passes
- [ ] Activation tested
- [ ] Forward slashes in paths
- [ ] No information Claude already knows
