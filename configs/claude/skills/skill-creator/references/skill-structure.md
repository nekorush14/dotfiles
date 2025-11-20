# Claude Code Agent Skills: Structure Reference

Detailed specification for skill directory structure, file formats, and organization patterns.

## Table of Contents

- [Directory Structure](#directory-structure)
- [SKILL.md Format](#skillmd-format)
- [YAML Frontmatter Specification](#yaml-frontmatter-specification)
- [Scripts Directory](#scripts-directory)
- [References Directory](#references-directory)
- [Assets Directory](#assets-directory)
- [Naming Conventions](#naming-conventions)
- [File Organization Patterns](#file-organization-patterns)

## Directory Structure

### Minimal Skill

```
skill-name/
└── SKILL.md              # Required: Main skill definition
```

### Complete Skill

```
skill-name/
├── SKILL.md              # Required: Main skill definition with YAML frontmatter
├── scripts/              # Optional: Executable utilities
│   ├── init.py           # Initialization script
│   ├── validate.py       # Validation script
│   └── helper.sh         # Shell helper script
├── references/           # Optional: Detailed documentation (loaded on demand)
│   ├── api-reference.md  # API documentation
│   ├── examples.md       # Extended examples
│   └── patterns.md       # Advanced patterns
└── assets/               # Optional: Templates and resources (not loaded into context)
    ├── template.yaml     # Configuration template
    └── schema.json       # JSON schema
```

## SKILL.md Format

### Basic Structure

```markdown
---
name: skill-name
description: What it does and when to use it
---

# Skill Title

Main content here...
```

### Complete Template

```markdown
---
name: skill-name
description: Detailed description with activation triggers
allowed-tools: [Read, Write, Edit, Bash]
metadata:
  category: backend
  language: python
---

# Skill Title

Brief overview of the skill's purpose.

## When to Use This Skill

- Specific scenario 1
- Specific scenario 2
- Specific scenario 3

## Core Principles

- **Principle 1**: Explanation
- **Principle 2**: Explanation
- **Principle 3**: Explanation

## Implementation Guidelines

### Pattern 1

Description and code example.

### Pattern 2

Description and code example.

## Tools to Use

- Tool 1: Usage description
- Tool 2: Usage description

### Common Commands

```bash
command examples
```

## Workflow

1. Step 1
2. Step 2
3. Step 3

## Related Skills

- `related-skill-1`: Relationship description
- `related-skill-2`: Relationship description

## Reference Documentation

- [Reference 1](references/file1.md)
- [Reference 2](references/file2.md)

## Key Reminders

- Reminder 1
- Reminder 2
- Reminder 3
```

## YAML Frontmatter Specification

### Required Fields

#### name

**Type**: `string`

**Requirements**:
- Lowercase letters, numbers, hyphens only
- Cannot start or end with hyphen
- No consecutive hyphens
- Max 64 characters
- No XML tags
- No reserved words: "anthropic", "claude"

**Valid Examples**:
```yaml
name: python-core-development
name: rails-service-objects
name: api-testing
name: pdf-processing
```

**Invalid Examples**:
```yaml
name: Python-Development    # Uppercase not allowed
name: -my-skill             # Cannot start with hyphen
name: my--skill             # Consecutive hyphens
name: my_skill              # Underscores not allowed
name: claude-helper         # Reserved word
```

#### description

**Type**: `string`

**Requirements**:
- Max 1024 characters
- No XML tags (< or >)
- Must include activation triggers
- Written in third person

**Format**: `[Functionality]. Use when [triggers].`

**Valid Examples**:
```yaml
description: Implement Python code with dataclasses, type hints, protocols, error handling, and async programming. Use when designing classes, implementing type safety, handling exceptions, or writing async code.
```

```yaml
description: Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDF files or when the user mentions PDFs.
```

**Invalid Examples**:
```yaml
description: Python tool                           # Too vague, no triggers
description: Helps with backend development        # No "Use when" clause
description: API tool <for testing>                # Contains XML tags
```

### Optional Fields

#### allowed-tools

**Type**: `array` of `string`

**Purpose**: Restrict which tools Claude can use within this skill.

**Available Tools**:
- `Read` - Read files
- `Write` - Create new files
- `Edit` - Modify existing files
- `Bash` - Execute bash commands
- `Glob` - Find files by pattern
- `Grep` - Search file contents
- `WebFetch` - Fetch web content
- `TodoWrite` - Manage todo list
- `AskUserQuestion` - Ask user questions

**Example**:
```yaml
allowed-tools: [Read, Write, Edit, Bash]
```

**Use Cases**:
- Security: Prevent file deletion or system commands
- Focus: Keep skill on specific operations
- Safety: Avoid unintended side effects

#### metadata

**Type**: `object`

**Purpose**: Additional organizational metadata.

**Common Fields**:
```yaml
metadata:
  category: backend | frontend | testing | devops
  language: python | ruby | typescript | javascript
  framework: rails | fastapi | react | nextjs
  complexity: beginner | intermediate | advanced
  version: 1.0.0
```

**Example**:
```yaml
metadata:
  category: backend
  language: python
  framework: fastapi
  complexity: intermediate
```

#### license

**Type**: `string`

**Purpose**: License information or reference.

**Examples**:
```yaml
license: MIT
license: Apache-2.0
license: Complete terms in LICENSE.txt
```

### Complete Frontmatter Example

```yaml
---
name: python-api-development
description: Implement REST APIs with FastAPI including endpoints, Pydantic models, validation, dependency injection, and error handling. Use when building API endpoints, request validation, or authentication.
allowed-tools: [Read, Write, Edit, Bash, WebFetch]
metadata:
  category: backend
  language: python
  framework: fastapi
  complexity: intermediate
  version: 1.0.0
license: MIT
---
```

## Scripts Directory

### Purpose

Executable utilities that:
- Automate repetitive tasks
- Perform validations
- Generate code or configuration
- Process data

### Naming Conventions

- `init_*.py` - Initialization scripts
- `validate_*.py` - Validation scripts
- `generate_*.py` - Code generation
- `process_*.py` - Data processing
- `*.sh` - Shell scripts

### Script Requirements

**Every script must**:
1. Have executable permissions (`chmod +x`)
2. Include shebang line (`#!/usr/bin/env python3`)
3. Have docstring with usage example
4. Handle errors explicitly
5. Provide helpful error messages
6. Document all constants and "magic numbers"

### Example Script Structure

```python
#!/usr/bin/env python3
"""
Brief description of what the script does.

Usage:
    python script_name.py <arg1> [--option <value>]

Example:
    python script_name.py my-input --format json
"""

import argparse
import sys
from pathlib import Path
from typing import Optional


def main_function(arg: str, option: Optional[str] = None) -> bool:
    """
    Main function with clear docstring.

    Args:
        arg: Description of argument
        option: Description of optional parameter

    Returns:
        True if successful, False otherwise

    Raises:
        ValueError: If arg is invalid
    """
    try:
        # Implementation with error handling
        result = process(arg, option)
        print(f"✅ Success: {result}")
        return True

    except ValueError as e:
        print(f"❌ Error: {e}")
        return False

    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Script description",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python script.py input1
  python script.py input2 --option value
        """
    )

    parser.add_argument("arg", help="Argument description")
    parser.add_argument("--option", help="Option description")

    args = parser.parse_args()

    success = main_function(args.arg, args.option)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
```

### Common Script Patterns

**Initialization Script**:
```python
# init_skill.py
# Creates directory structure and template files
```

**Validation Script**:
```python
# validate_skill.py
# Checks YAML frontmatter and file structure
```

**Code Generation Script**:
```python
# generate_test.py
# Generates test files from templates
```

## References Directory

### Purpose

Detailed documentation loaded on demand:
- API specifications
- Extended examples
- Advanced patterns
- Domain-specific guides

### Naming Conventions

Use descriptive, hyphenated names:
- `api-reference.md` - API documentation
- `best-practices.md` - Best practices guide
- `examples.md` - Extended examples
- `advanced-patterns.md` - Advanced techniques
- `troubleshooting.md` - Common issues and solutions

### File Requirements

**Every reference file must**:
1. Include table of contents (if >100 lines)
2. Use descriptive section headers
3. Provide concrete examples
4. Stay focused on single topic
5. Use forward slashes in paths

### Reference File Template

```markdown
# Reference Title

Brief overview of what this reference covers.

## Table of Contents

- [Section 1](#section-1)
- [Section 2](#section-2)
- [Section 3](#section-3)

## Section 1

Detailed content with examples.

### Subsection 1.1

Content here.

## Section 2

More detailed content.

## Section 3

Additional information.
```

### Organization Patterns

**Single Topic per File**:
```
references/
├── authentication.md      # Auth patterns only
├── validation.md          # Validation patterns only
└── error-handling.md      # Error handling only
```

**Progressive Complexity**:
```
references/
├── basic-patterns.md      # Beginner patterns
├── intermediate-patterns.md  # Intermediate patterns
└── advanced-patterns.md   # Advanced patterns
```

**Domain-Based**:
```
references/
├── users-api.md           # User-related endpoints
├── products-api.md        # Product-related endpoints
└── orders-api.md          # Order-related endpoints
```

## Assets Directory

### Purpose

Non-context resources:
- Configuration templates
- JSON schemas
- Example files
- Media files

**Important**: Files in assets/ are **NOT automatically loaded** into Claude's context.

### Use Cases

1. **Templates**: Configuration file templates
2. **Schemas**: JSON/YAML schemas for validation
3. **Examples**: Example input/output files
4. **Media**: Images, fonts (if needed by scripts)

### Example Structure

```
assets/
├── templates/
│   ├── config.yaml.template
│   └── dockerfile.template
├── schemas/
│   ├── request.schema.json
│   └── response.schema.json
└── examples/
    ├── input-example.json
    └── output-example.json
```

### Asset Naming

Use descriptive names with extensions:
- `config.yaml.template` - Configuration template
- `*.schema.json` - JSON schemas
- `example-*.json` - Example files
- `sample-*.md` - Sample documents

## Naming Conventions

### Skill Names

**Format**: `domain-action` or `domain-technology`

**Action-Based** (use gerund form):
```
processing-pdfs
analyzing-data
generating-reports
testing-apis
```

**Domain-Based**:
```
python-core-development
rails-service-objects
react-components
nextjs-optimization
```

**Avoid**:
- Generic terms: `helper`, `utils`, `tools`
- Vague names: `backend`, `frontend`
- Camel case: `apiTesting`
- Underscores: `api_testing`

### File Names

**SKILL.md**: Always uppercase

**Scripts**: Lowercase with underscores
```
init_skill.py
validate_skill.py
generate_test.py
```

**References**: Lowercase with hyphens
```
api-reference.md
best-practices.md
advanced-patterns.md
```

**Assets**: Descriptive with extensions
```
config.yaml.template
request.schema.json
example-input.json
```

## File Organization Patterns

### Pattern 1: Simple Skill

For focused skills with minimal content (<300 lines):

```
skill-name/
└── SKILL.md
```

### Pattern 2: Standard Skill

For skills with utility scripts:

```
skill-name/
├── SKILL.md
└── scripts/
    ├── init.py
    └── validate.py
```

### Pattern 3: Documented Skill

For skills needing extended documentation:

```
skill-name/
├── SKILL.md
├── references/
│   ├── api-reference.md
│   └── examples.md
└── scripts/
    └── helper.py
```

### Pattern 4: Complete Skill

For complex skills with all components:

```
skill-name/
├── SKILL.md
├── scripts/
│   ├── init.py
│   ├── validate.py
│   └── generate.py
├── references/
│   ├── api-reference.md
│   ├── best-practices.md
│   └── examples.md
└── assets/
    ├── templates/
    │   └── config.template
    └── schemas/
        └── schema.json
```

## Path Conventions

### Always Use Forward Slashes

**Correct**:
```python
path = "configs/claude/skills/my-skill"
```

**Incorrect**:
```python
path = "configs\\claude\\skills\\my-skill"  # Windows-style
```

### Relative vs Absolute Paths

**In Documentation** - Use relative paths from skill root:
```markdown
See [API Reference](references/api-reference.md)
```

**In Scripts** - Use Path for cross-platform compatibility:
```python
from pathlib import Path

skill_dir = Path(__file__).parent.parent
ref_file = skill_dir / "references" / "api-reference.md"
```

## Size Guidelines

| Component | Recommended Size | Maximum Size |
|-----------|-----------------|--------------|
| SKILL.md | 200-400 lines | 500 lines |
| Reference file | 200-400 lines | 500 lines |
| Script | 100-300 lines | 500 lines |
| Total skill | <2000 lines | 3000 lines |

**When to split**:
- SKILL.md >500 lines → Move content to references/
- Reference file >500 lines → Split into multiple files
- Skill >3000 total lines → Consider splitting into multiple skills

## Validation Checklist

**Structure**:
- [ ] SKILL.md exists in root
- [ ] YAML frontmatter is valid
- [ ] Required fields present (name, description)
- [ ] Optional directories exist if referenced
- [ ] No nested subdirectories in references/

**Naming**:
- [ ] Skill name: lowercase, hyphens, <64 chars
- [ ] Files use appropriate naming convention
- [ ] No spaces in filenames
- [ ] Forward slashes in all paths

**Content**:
- [ ] SKILL.md <500 lines
- [ ] References have table of contents
- [ ] Scripts have docstrings and error handling
- [ ] Examples include WHY comments

**Metadata**:
- [ ] Description includes "Use when" clause
- [ ] Description <1024 chars, no XML tags
- [ ] allowed-tools (if present) are valid
- [ ] metadata (if present) uses standard fields
