#!/usr/bin/env python3
"""
Validate Claude Code Agent Skill format and requirements.

Usage:
    python validate_skill.py <skill-directory>

Example:
    python validate_skill.py configs/claude/skills/my-skill
"""

import argparse
import re
import sys
from pathlib import Path
from typing import Optional, Dict, Any

try:
    import yaml
except ImportError:
    print("❌ Error: PyYAML is required. Install with: pip install pyyaml")
    sys.exit(1)


ALLOWED_PROPERTIES = {
    "name",
    "description",
    "license",
    "allowed-tools",
    "metadata"
}


def validate_name(name: str) -> tuple[bool, Optional[str]]:
    """
    Validate skill name format.

    Requirements:
    - Max 64 characters
    - Lowercase letters, numbers, and hyphens only
    - Cannot start or end with hyphen
    - No consecutive hyphens
    - No reserved words

    Returns:
        (is_valid, error_message)
    """
    if not name:
        return False, "Name is empty"

    if len(name) > 64:
        return False, f"Name too long: {len(name)} chars (max 64)"

    if name.startswith("-") or name.endswith("-"):
        return False, "Name cannot start or end with hyphen"

    if "--" in name:
        return False, "Name cannot contain consecutive hyphens"

    # WHY: Ensure only valid characters
    if not re.match(r"^[a-z0-9-]+$", name):
        return False, "Name must contain only lowercase letters, numbers, and hyphens"

    # Reserved words check
    reserved_words = ["anthropic", "claude"]
    name_lower = name.lower()
    for word in reserved_words:
        if word in name_lower:
            return False, f"Name cannot contain reserved word: {word}"

    return True, None


def validate_description(description: str) -> tuple[bool, Optional[str]]:
    """
    Validate skill description.

    Requirements:
    - Must be non-empty string
    - Max 1024 characters
    - No XML tags (< or >)

    Returns:
        (is_valid, error_message)
    """
    if not isinstance(description, str):
        return False, f"Description must be string, got {type(description).__name__}"

    if not description.strip():
        return False, "Description is empty"

    if len(description) > 1024:
        return False, f"Description too long: {len(description)} chars (max 1024)"

    # WHY: Prevent XML injection or parsing issues
    if "<" in description or ">" in description:
        return False, "Description cannot contain angle brackets (< or >)"

    return True, None


def validate_allowed_tools(tools: Any) -> tuple[bool, Optional[str]]:
    """
    Validate allowed-tools field.

    Requirements:
    - Must be a list if present
    - Each tool must be a string

    Returns:
        (is_valid, error_message)
    """
    if not isinstance(tools, list):
        return False, f"allowed-tools must be a list, got {type(tools).__name__}"

    for tool in tools:
        if not isinstance(tool, str):
            return False, f"Tool name must be string, got {type(tool).__name__}"

    return True, None


def parse_frontmatter(content: str) -> tuple[Optional[Dict[str, Any]], Optional[str]]:
    """
    Parse YAML frontmatter from SKILL.md content.

    Args:
        content: Full SKILL.md file content

    Returns:
        (frontmatter_dict, error_message)
    """
    # WHY: YAML frontmatter is delimited by --- markers
    parts = content.split("---", 2)

    if len(parts) < 3:
        return None, "No YAML frontmatter found (must be delimited by ---)"

    frontmatter_text = parts[1].strip()

    try:
        frontmatter = yaml.safe_load(frontmatter_text)

        if not isinstance(frontmatter, dict):
            return None, "Frontmatter must be a YAML dictionary"

        return frontmatter, None

    except yaml.YAMLError as e:
        return None, f"Invalid YAML syntax: {e}"


def validate_skill(skill_path: str) -> bool:
    """
    Validate a Claude Code Agent Skill.

    Args:
        skill_path: Path to skill directory

    Returns:
        True if valid, False otherwise
    """
    skill_dir = Path(skill_path)

    # Check if directory exists
    if not skill_dir.exists():
        print(f"❌ Error: Directory not found: {skill_dir}")
        return False

    if not skill_dir.is_dir():
        print(f"❌ Error: Not a directory: {skill_dir}")
        return False

    # Check if SKILL.md exists
    skill_file = skill_dir / "SKILL.md"
    if not skill_file.exists():
        print(f"❌ Error: SKILL.md not found in {skill_dir}")
        return False

    # Read SKILL.md
    try:
        content = skill_file.read_text(encoding="utf-8")
    except Exception as e:
        print(f"❌ Error reading SKILL.md: {e}")
        return False

    # Parse frontmatter
    frontmatter, error = parse_frontmatter(content)
    if error:
        print(f"❌ Frontmatter error: {error}")
        return False

    # Check for unknown properties
    unknown_props = set(frontmatter.keys()) - ALLOWED_PROPERTIES
    if unknown_props:
        print(f"⚠️  Warning: Unknown properties: {', '.join(unknown_props)}")

    # Validate required fields
    has_errors = False

    # Validate name
    if "name" not in frontmatter:
        print(f"❌ Error: Required field 'name' is missing")
        has_errors = True
    else:
        is_valid, error = validate_name(frontmatter["name"])
        if not is_valid:
            print(f"❌ Name validation error: {error}")
            has_errors = True
        else:
            print(f"✅ Name: {frontmatter['name']}")

    # Validate description
    if "description" not in frontmatter:
        print(f"❌ Error: Required field 'description' is missing")
        has_errors = True
    else:
        is_valid, error = validate_description(frontmatter["description"])
        if not is_valid:
            print(f"❌ Description validation error: {error}")
            has_errors = True
        else:
            desc_len = len(frontmatter["description"])
            print(f"✅ Description: {desc_len} chars")

            # Check if description includes "Use when"
            if "use when" not in frontmatter["description"].lower():
                print(f"⚠️  Warning: Description should include 'Use when' clause for activation triggers")

    # Validate optional fields
    if "allowed-tools" in frontmatter:
        is_valid, error = validate_allowed_tools(frontmatter["allowed-tools"])
        if not is_valid:
            print(f"❌ allowed-tools validation error: {error}")
            has_errors = True
        else:
            tool_count = len(frontmatter["allowed-tools"])
            print(f"✅ allowed-tools: {tool_count} tools")

    # Check file size
    file_size = len(content)
    line_count = content.count("\n")
    print(f"📊 File size: {file_size} bytes, {line_count} lines")

    if line_count > 500:
        print(f"⚠️  Warning: SKILL.md is {line_count} lines (recommended: <500)")
        print(f"   Consider moving content to references/ directory")

    # Summary
    print("\n" + "="*60)
    if has_errors:
        print("❌ Validation FAILED")
        print("="*60)
        return False
    else:
        print("✅ Validation PASSED")
        print("="*60)
        print("\nOptional checks:")
        print("- Test activation with trigger phrases")
        print("- Verify examples are concrete and minimal")
        print("- Check that code examples include WHY comments")
        print("- Ensure references/ files have table of contents")
        return True


def main():
    """Main entry point for CLI."""
    parser = argparse.ArgumentParser(
        description="Validate Claude Code Agent Skill format",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python validate_skill.py configs/claude/skills/my-skill
  python validate_skill.py ~/skills/python-testing
        """
    )

    parser.add_argument(
        "skill_path",
        help="Path to skill directory"
    )

    args = parser.parse_args()

    is_valid = validate_skill(args.skill_path)
    sys.exit(0 if is_valid else 1)


if __name__ == "__main__":
    main()
