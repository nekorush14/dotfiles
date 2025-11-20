---
name: skill-creator
description: Guide for creating effective Agent Skills. Use when creating a new skill (or updating an existing skill) that extends capabilities with specialized knowledge, workflows, or tool integrations. Helps with skill initialization, validation, and best practices.
license: Complete terms in LICENSE
---

# Claude Code Skill Creator

Specialized in creating effective, well-structured Claude Code Agent Skills following best practices and design patterns.

## When to Use This Skill

- Creating a new Claude Code Agent Skill from scratch
- Updating or refactoring existing skills
- Understanding skill structure and YAML frontmatter requirements
- Implementing progressive disclosure patterns
- Validating skill format and requirements
- Following skill authoring best practices

## Core Principles

- **Context Window is a Public Good**: Keep content concise and essential
- **Progressive Disclosure**: Structure information in layers (metadata → body → references)
- **Appropriate Freedom**: Match specificity to task fragility
- **Clear Activation Triggers**: Description must specify both function and when to use
- **Single Responsibility**: One skill per capability or domain
- **Concrete Examples**: Provide specific input/output examples

## Skill Anatomy

### Required Structure

```
skill-name/
├── SKILL.md              # Required: Main skill definition
├── scripts/              # Optional: Executable utilities (Python, Bash)
├── references/           # Optional: Detailed documentation
└── assets/               # Optional: Templates, non-context resources
```

### SKILL.md Format

```yaml
---
name: skill-name
description: What it does and when to use it (max 1024 chars)
allowed-tools: [optional list]  # Optional: Restrict tool access
---

# Skill Title

## When to Use This Skill
- Specific trigger scenarios

## Core Principles
- Guiding design principles

## Implementation Guidelines
- Detailed instructions with examples

## Tools to Use
- Tool usage patterns

## Workflow
- Step-by-step process

## Related Skills
- Cross-references to other skills
```

## YAML Frontmatter Requirements

### Required Fields

**name** (required):

- Max 64 characters
- Lowercase letters, numbers, hyphens only
- Cannot start/end with hyphens
- No consecutive hyphens
- No XML tags or reserved words ("anthropic", "claude")

Example: `python-core-development`, `rails-service-objects`

**description** (required):

- Max 1024 characters
- No XML tags (< or >)
- Must specify both functionality AND activation triggers
- Written in third person

Good example:

```
description: Implement Python code with dataclasses, type hints, protocols, error handling, and async programming. Use when designing classes, implementing type safety, handling exceptions, or writing async code.
```

Bad example:

```
description: Helps with Python development
```

### Optional Fields

**allowed-tools**: Restrict Claude's tool access within this skill

```yaml
allowed-tools: [Read, Grep, Glob, Write, Edit, Bash, WebFetch]
```

**metadata**: Additional metadata for skill organization

```yaml
metadata:
  category: backend
  language: python
  complexity: intermediate
```

## Progressive Disclosure Design

Structure skills in three levels to manage context efficiently:

### Level 1: Metadata (Always Loaded)

- name and description in YAML frontmatter
- Claude uses this to decide whether to activate the skill

### Level 2: Skill Body (Loaded When Activated)

- Overview and core principles (50-150 lines)
- Essential guidelines and patterns
- Common use cases
- Keep main file under 500 lines

### Level 3: References (Loaded On Demand)

- Detailed documentation in references/ directory
- API specifications
- Extended examples
- One level deep maximum (no nested directories)

Example:

```
skill-name/
├── SKILL.md                    # Level 2: Core guidance
├── references/
│   ├── api-reference.md        # Level 3: API details
│   ├── advanced-patterns.md    # Level 3: Advanced techniques
│   └── examples.md             # Level 3: Extended examples
```

## Skill Creation Workflow

### 1. Planning

- Define the skill's single responsibility
- Identify trigger scenarios
- Determine required tools
- Plan progressive disclosure structure

### 2. Initialize Skill

Use the init_skill.py script:

```bash
python configs/claude/skills/claude-code-skill-creator/scripts/init_skill.py skill-name --path configs/claude/skills
```

This creates:

- Directory structure
- SKILL.md template with TODOs
- Placeholder directories

### 3. Write SKILL.md

**Structure your content**:

1. **When to Use This Skill**: Clear trigger scenarios
2. **Core Principles**: 3-6 guiding principles
3. **Implementation Guidelines**: Concrete patterns with code examples
4. **Tools to Use**: Specific tool usage
5. **Workflow**: Step-by-step process
6. **Related Skills**: Cross-references

**Best practices**:

- Use code examples for every pattern
- Include WHY comments in code
- Keep examples focused and minimal
- Reference related skills
- Stay under 500 lines

### 4. Add Reference Files

Create references/ files for:

- Detailed API documentation
- Advanced patterns
- Extended examples
- Domain-specific guides

Include table of contents for long reference files.

### 5. Add Utility Scripts

Create scripts/ for:

- Code generation
- Validation
- Data processing
- Common operations

Requirements:

- Explicit error handling
- Helpful error messages
- Document all constants
- List required packages
- Executable permissions (chmod +x)

### 6. Validate Skill

```bash
python configs/claude/skills/claude-code-skill-creator/scripts/validate_skill.py configs/claude/skills/skill-name
```

Checks:

- SKILL.md exists
- Valid YAML frontmatter
- Required fields present
- Name format correct
- Description within limits

### 7. Test and Iterate

- Test with Claude using trigger phrases from description
- Verify Claude discovers and activates the skill
- Refine based on actual usage patterns
- Iterate on description for better activation

## Naming Conventions

### Skill Names

Use gerund form (verb + -ing) for action-based skills:

- ✓ `processing-pdfs`, `analyzing-data`, `generating-reports`
- ✗ `pdf-processor`, `data-analyzer`, `report-generator`

Use domain-noun for knowledge/reference skills:

- ✓ `python-core-development`, `rails-security`, `react-components`

Avoid:

- Vague terms: `helper`, `utils`, `tools`
- Generic names: `backend`, `frontend`
- Overly broad: `programming`, `development`

### File Names

References:

- `api-reference.md` - API documentation
- `best-practices.md` - Best practices guide
- `examples.md` - Extended examples
- `advanced-patterns.md` - Advanced techniques

Scripts:

- `init_*.py` - Initialization scripts
- `validate_*.py` - Validation scripts
- `generate_*.py` - Generation scripts

## Common Anti-Patterns

### ❌ Avoid

**Vague descriptions**:

```yaml
description: Helps with Python development
```

**Information Claude already knows**:

```markdown
Python uses indentation for code blocks...
```

**Overly complex main file** (>500 lines):

```markdown
SKILL.md with 1000+ lines of content
```

**Multiple responsibilities**:

```yaml
name: backend-development  # Too broad
description: Handle all backend tasks
```

**Windows-style paths**:

```python
path = "configs\\claude\\skills"  # Wrong
```

### ✓ Use Instead

**Specific descriptions with triggers**:

```yaml
description: Implement Python code with dataclasses, type hints, protocols, error handling, and async programming. Use when designing classes, implementing type safety, handling exceptions, or writing async code.
```

**Progressive disclosure**:

```markdown
SKILL.md (300 lines) → references/api-reference.md → references/examples.md
```

**Single responsibility**:

```yaml
name: python-core-development
description: Core Python class design and type safety
```

**Forward slashes**:

```python
path = "configs/claude/skills"  # Correct
```

## Effective Description Writing

Description format: `[What it does]. Use when [trigger scenarios].`

Examples:

**Good**:

```
description: Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDF files or when the user mentions PDFs.
```

**Good**:

```
description: Implement Python code with dataclasses, type hints, protocols, error handling, and async programming. Use when designing classes, implementing type safety, handling exceptions, or writing async code.
```

**Bad** (missing triggers):

```
description: Python development tool
```

**Bad** (too vague):

```
description: Helps with backend tasks
```

## Tools to Use

- `Read`: Read existing skills for reference
- `Write`: Create new SKILL.md and reference files
- `Edit`: Modify existing skill files
- `Bash`: Run Python scripts (init, validate)
- `Glob`: Find existing skills by pattern
- `Grep`: Search for patterns in skills

### Common Commands

```bash
# Initialize new skill
python configs/claude/skills/claude-code-skill-creator/scripts/init_skill.py new-skill-name --path configs/claude/skills

# Validate skill
python configs/claude/skills/claude-code-skill-creator/scripts/validate_skill.py configs/claude/skills/new-skill-name

# Find all skills
ls configs/claude/skills/

# Search for patterns in skills
grep -r "description:" configs/claude/skills/*/SKILL.md

# Check skill structure
tree configs/claude/skills/new-skill-name
```

## Workflow

1. **Define Scope**: Clarify skill's single responsibility
2. **Plan Structure**: Decide on main file vs. references split
3. **Initialize**: Run init_skill.py script
4. **Write SKILL.md**: Fill in template with examples
5. **Add References**: Create reference files if needed
6. **Add Scripts**: Create utility scripts if needed
7. **Validate**: Run validate_skill.py
8. **Test**: Try activating skill with trigger phrases
9. **Iterate**: Refine based on usage
10. **Document**: Update README.md with skill entry

## Related Skills

This skill helps create other skills. Once created, skills may reference:

- Domain-specific skills (python-core-development, rails-service-objects)
- Testing skills (pytest-testing, rspec-model-testing)
- Framework skills (react-component-development, nextjs-app-development)

## Reference Documentation

See detailed documentation in references/:

- [Best Practices](references/best-practices.md) - Comprehensive best practices
- [Skill Structure](references/skill-structure.md) - Detailed structure guide

## Key Reminders

- Keep SKILL.md under 500 lines
- Include both "what" and "when" in description
- Provide concrete code examples
- Use progressive disclosure (main → references → assets)
- Validate with scripts before use
- Test activation with trigger phrases
- Use forward slashes in all paths
- Single responsibility per skill
- Gerund form for action-based skill names
- Reference related skills for cross-functionality
