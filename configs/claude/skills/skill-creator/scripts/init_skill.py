#!/usr/bin/env python3
"""
Initialize a new Claude Code Agent Skill with proper directory structure.

Usage:
    python init_skill.py <skill-name> [--path <path>]

Example:
    python init_skill.py my-new-skill --path configs/claude/skills
"""

import argparse
import os
import sys
from pathlib import Path
from typing import Optional


SKILL_TEMPLATE = """---
name: {skill_name}
description: TODO: Describe what this skill does and when to use it (max 1024 chars). Include both functionality and activation triggers.
---

# {skill_title}

TODO: Add a brief overview of what this skill specializes in.

## When to Use This Skill

TODO: List specific scenarios when this skill should be activated:
- Scenario 1
- Scenario 2
- Scenario 3

## Core Principles

TODO: Define 3-6 guiding principles for this skill:
- **Principle 1**: Brief explanation
- **Principle 2**: Brief explanation
- **Principle 3**: Brief explanation

## Implementation Guidelines

TODO: Provide concrete patterns with code examples.

### Pattern 1

```
# WHY: Explain why this pattern is used
code example here
```

### Pattern 2

```
# WHY: Explain why this pattern is used
code example here
```

## Tools to Use

TODO: Specify which tools this skill should use:
- `Read`: For reading files
- `Write`: For creating files
- `Edit`: For modifying files
- `Bash`: For running commands
- `Grep`: For searching content
- `Glob`: For finding files

### Common Commands

```bash
# TODO: Add common bash commands
command example
```

## Workflow

TODO: Define step-by-step process:
1. **Step 1**: Description
2. **Step 2**: Description
3. **Step 3**: Description

## Related Skills

TODO: List related skills:
- `related-skill-1`: Brief description of relation
- `related-skill-2`: Brief description of relation

## Reference Documentation

TODO: If you created reference files, link them here:
- [Reference Title](references/reference-file.md) - Description

## Key Reminders

TODO: List essential reminders:
- Reminder 1
- Reminder 2
- Reminder 3
"""


def to_title_case(skill_name: str) -> str:
    """
    Convert hyphenated skill name to Title Case.

    Example: my-skill-name -> My Skill Name
    """
    return " ".join(word.capitalize() for word in skill_name.split("-"))


def validate_skill_name(name: str) -> bool:
    """
    Validate skill name format.

    Requirements:
    - Lowercase letters, numbers, and hyphens only
    - Cannot start or end with hyphen
    - No consecutive hyphens
    - Max 64 characters
    """
    if not name:
        return False

    if len(name) > 64:
        print(f"❌ Error: Skill name too long (max 64 characters)")
        return False

    if name.startswith("-") or name.endswith("-"):
        print(f"❌ Error: Skill name cannot start or end with hyphen")
        return False

    if "--" in name:
        print(f"❌ Error: Skill name cannot contain consecutive hyphens")
        return False

    # WHY: Ensure only valid characters (lowercase, digits, hyphens)
    if not all(c.islower() or c.isdigit() or c == "-" for c in name):
        print(f"❌ Error: Skill name must contain only lowercase letters, numbers, and hyphens")
        return False

    return True


def init_skill(skill_name: str, base_path: Optional[str] = None) -> bool:
    """
    Initialize a new skill directory with template files.

    Args:
        skill_name: Name of the skill (hyphenated, lowercase)
        base_path: Base directory for skills (default: current directory)

    Returns:
        True if successful, False otherwise
    """
    # Validate skill name
    if not validate_skill_name(skill_name):
        return False

    # Resolve base path
    if base_path:
        skill_dir = Path(base_path) / skill_name
    else:
        skill_dir = Path.cwd() / skill_name

    # Check if directory already exists
    if skill_dir.exists():
        print(f"❌ Error: Directory already exists: {skill_dir}")
        return False

    try:
        # Create main directory
        skill_dir.mkdir(parents=True, exist_ok=False)
        print(f"✅ Created directory: {skill_dir}")

        # Create subdirectories
        (skill_dir / "scripts").mkdir()
        (skill_dir / "references").mkdir()
        (skill_dir / "assets").mkdir()
        print(f"✅ Created subdirectories: scripts/, references/, assets/")

        # Create SKILL.md from template
        skill_title = to_title_case(skill_name)
        skill_content = SKILL_TEMPLATE.format(
            skill_name=skill_name,
            skill_title=skill_title
        )

        skill_file = skill_dir / "SKILL.md"
        skill_file.write_text(skill_content)
        print(f"✅ Created SKILL.md with template")

        # Create .keep files to maintain directory structure
        (skill_dir / "scripts" / ".keep").touch()
        print(f"✅ Created scripts/.keep")

        (skill_dir / "references" / ".keep").touch()
        print(f"✅ Created references/.keep")

        (skill_dir / "assets" / ".keep").touch()
        print(f"✅ Created assets/.keep")

        # Success message
        print("\n" + "="*60)
        print(f"🎉 Successfully initialized skill: {skill_name}")
        print("="*60)
        print("\nNext steps:")
        print(f"1. Edit {skill_file} and fill in TODO sections")
        print(f"2. Update the 'description' field with clear activation triggers")
        print(f"3. Add concrete examples and code patterns")
        print(f"4. Create reference files in references/ if needed")
        print(f"5. Add utility scripts in scripts/ if needed")
        print(f"6. Validate with: python validate_skill.py {skill_dir}")
        print(f"7. Test by using trigger phrases from your description")

        return True

    except Exception as e:
        print(f"❌ Error creating skill: {e}")
        # WHY: Clean up partial directory on failure
        if skill_dir.exists():
            import shutil
            shutil.rmtree(skill_dir)
        return False


def main():
    """Main entry point for CLI."""
    parser = argparse.ArgumentParser(
        description="Initialize a new Claude Code Agent Skill",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python init_skill.py my-skill
  python init_skill.py python-api-testing --path configs/claude/skills
  python init_skill.py data-processing --path ~/skills
        """
    )

    parser.add_argument(
        "skill_name",
        help="Name of the skill (lowercase, hyphens, max 64 chars)"
    )

    parser.add_argument(
        "--path",
        help="Base directory for skills (default: current directory)",
        default=None
    )

    args = parser.parse_args()

    success = init_skill(args.skill_name, args.path)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
