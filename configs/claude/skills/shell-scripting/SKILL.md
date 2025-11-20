---
name: shell-scripting
description: Write and optimize Bash, Zsh, and shell scripts with best practices for error handling, argument parsing, portability, and security. Use when writing shell scripts, debugging scripts, implementing command-line tools, or improving shell script maintainability and security.
---

# Shell Scripting

Provides best practices, patterns, and security guidelines for Bash, Zsh, and general shell script development. Helps create maintainable, secure, and portable shell scripts.

## When to Use This Skill

- Writing or modifying shell scripts
- Implementing Bash or Zsh-specific features
- Improving error handling in shell scripts
- Implementing argument parsing and option handling
- Creating cross-platform compatible scripts
- Debugging or troubleshooting shell scripts
- Fixing security vulnerabilities in scripts

## Core Principles

- **Fail Fast**: Exit immediately on errors with clear error messages
- **Defensive Programming**: Validate inputs and anticipate unexpected situations
- **POSIX Compatibility**: Maintain POSIX compliance when possible for portability
- **Explicit Error Handling**: Handle all error cases explicitly
- **Secure by Default**: Use secure defaults to minimize security risks
- **Readability Over Cleverness**: Prioritize readability over clever tricks

## Implementation Guidelines

### Script Header and Setup

Start all scripts with proper headers and settings:

```bash
#!/usr/bin/env bash
# WHY: Use 'env' to find bash in PATH, improving portability

set -euo pipefail
# WHY: -e exits on error, -u treats unset variables as errors,
#      -o pipefail ensures pipe failures are caught

# Optional: Enable debug mode
# set -x  # WHY: Prints each command before execution for debugging
```

### Error Handling

Implement thorough error handling:

```bash
# WHY: Trap errors and cleanup resources before exit
cleanup() {
  local exit_code=$?
  # WHY: Perform cleanup even on error
  rm -f "$temp_file"
  exit "$exit_code"
}
trap cleanup EXIT ERR

# WHY: Check command success explicitly when needed
if ! command -v git &> /dev/null; then
  echo "Error: git is not installed" >&2
  exit 1
fi

# WHY: Use logical operators for simple error handling
mkdir -p "$dir" || { echo "Failed to create directory" >&2; exit 1; }
```

### Variable Handling

Handle variables safely:

```bash
# WHY: Always quote variables to prevent word splitting and globbing
file_path="/path/to/my file.txt"
cat "$file_path"  # Correct
# cat $file_path  # Wrong: breaks on spaces

# WHY: Use ${var:-default} for default values
output_dir="${OUTPUT_DIR:-./output}"

# WHY: Use ${var:?error} to require variables
database_url="${DATABASE_URL:?Error: DATABASE_URL must be set}"

# WHY: Use lowercase for local variables, UPPERCASE for environment/constants
local temp_file="/tmp/data.txt"
readonly CONFIG_FILE="/etc/app.conf"
```

### Argument Parsing

Parse arguments properly:

```bash
# WHY: Parse both short and long options
usage() {
  cat << EOF
Usage: $0 [OPTIONS]

Options:
  -h, --help       Show this help message
  -v, --verbose    Enable verbose output
  -o, --output DIR Output directory (default: ./output)
EOF
}

verbose=false
output_dir="./output"

while [[ $# -gt 0 ]]; do
  case "$1" in
    -h|--help)
      usage
      exit 0
      ;;
    -v|--verbose)
      verbose=true
      shift
      ;;
    -o|--output)
      # WHY: Validate argument exists
      if [[ -z "${2:-}" ]]; then
        echo "Error: --output requires an argument" >&2
        exit 1
      fi
      output_dir="$2"
      shift 2
      ;;
    -*)
      echo "Error: Unknown option: $1" >&2
      usage >&2
      exit 1
      ;;
    *)
      # WHY: Handle positional arguments
      break
      ;;
  esac
done
```

### Function Definition

Define functions clearly:

```bash
# WHY: Use 'local' to avoid polluting global scope
process_file() {
  local file_path="$1"
  local output_path="$2"

  # WHY: Validate required arguments
  if [[ -z "$file_path" || -z "$output_path" ]]; then
    echo "Error: process_file requires 2 arguments" >&2
    return 1
  fi

  # WHY: Check file exists before processing
  if [[ ! -f "$file_path" ]]; then
    echo "Error: File not found: $file_path" >&2
    return 1
  fi

  # Process file...

  # WHY: Return explicit exit codes
  return 0
}
```

### File and Directory Operations

Perform file operations safely:

```bash
# WHY: Always check before overwriting
if [[ -e "$output_file" ]]; then
  echo "Error: Output file already exists: $output_file" >&2
  exit 1
fi

# WHY: Use mktemp for temporary files
temp_file=$(mktemp) || { echo "Failed to create temp file" >&2; exit 1; }

# WHY: Create directories with -p (no error if exists)
mkdir -p "$output_dir" || exit 1

# WHY: Use pushd/popd for directory navigation
pushd "$target_dir" > /dev/null || exit 1
# Do work...
popd > /dev/null
```

### String Operations

Process strings safely:

```bash
# WHY: Use [[ ]] for string tests (safer than [ ])
if [[ "$var" == "value" ]]; then
  echo "Match"
fi

# WHY: Use regex matching with =~
if [[ "$email" =~ ^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$ ]]; then
  echo "Valid email"
fi

# WHY: Use parameter expansion for string manipulation
filename="document.pdf"
basename="${filename%.pdf}"      # document
extension="${filename##*.}"       # pdf
uppercase="${var^^}"              # Convert to uppercase (Bash 4+)
lowercase="${var,,}"              # Convert to lowercase (Bash 4+)
```

### Array Usage

Use arrays effectively:

```bash
# WHY: Declare arrays explicitly
declare -a files
files=("file1.txt" "file2.txt" "file3.txt")

# WHY: Use "${array[@]}" to expand all elements properly
for file in "${files[@]}"; do
  process_file "$file"
done

# WHY: Check array length
if [[ ${#files[@]} -eq 0 ]]; then
  echo "No files to process"
  exit 0
fi

# WHY: Use mapfile to read lines into array (Bash 4+)
mapfile -t lines < "$input_file"
```

### Conditional Execution

Use conditional execution appropriately:

```bash
# WHY: Use && and || for simple conditionals
[[ -f "$file" ]] && echo "File exists"
[[ ! -d "$dir" ]] && mkdir -p "$dir"

# WHY: Use if statements for complex logic
if [[ -f "$config_file" ]]; then
  source "$config_file"
elif [[ -f "$default_config" ]]; then
  source "$default_config"
else
  echo "Error: No config file found" >&2
  exit 1
fi
```

### Command Substitution

Use command substitution safely:

```bash
# WHY: Use $() instead of backticks (more readable, nestable)
current_date=$(date +%Y-%m-%d)
file_count=$(find . -type f | wc -l)

# WHY: Capture stderr separately when needed
output=$(command 2>&1) || {
  echo "Command failed: $output" >&2
  exit 1
}
```

### Logging and Output

Output logs appropriately:

```bash
# WHY: Write errors to stderr
log_error() {
  echo "ERROR: $*" >&2
}

log_info() {
  echo "INFO: $*"
}

log_debug() {
  # WHY: Only log debug messages when verbose mode is enabled
  if [[ "$verbose" == true ]]; then
    echo "DEBUG: $*" >&2
  fi
}

# Usage
log_info "Processing file: $file"
log_error "Failed to connect to database"
```

### Security Practices

Consider security:

```bash
# WHY: Never use eval with user input (command injection risk)
# eval "$user_input"  # DANGEROUS!

# WHY: Quote all variable expansions in commands
rm -f "$file"  # Correct
# rm -f $file  # Dangerous if $file contains spaces or special chars

# WHY: Use absolute paths for commands in production scripts
/usr/bin/git status  # Prevents PATH manipulation attacks

# WHY: Validate and sanitize user input
sanitize_filename() {
  local filename="$1"
  # WHY: Remove potentially dangerous characters
  filename="${filename//[^a-zA-Z0-9._-]/}"
  echo "$filename"
}

# WHY: Use secure permissions for sensitive files
chmod 600 "$credentials_file"
```

### Cross-Platform Compatibility

Consider cross-platform compatibility:

```bash
# WHY: Detect OS for platform-specific behavior
detect_os() {
  case "$(uname -s)" in
    Darwin*)
      echo "macos"
      ;;
    Linux*)
      echo "linux"
      ;;
    MINGW*|MSYS*)
      echo "windows"
      ;;
    *)
      echo "unknown"
      ;;
  esac
}

os_type=$(detect_os)

# WHY: Use portable commands when possible
# Use 'command -v' instead of 'which'
if command -v python3 &> /dev/null; then
  python_cmd="python3"
elif command -v python &> /dev/null; then
  python_cmd="python"
fi
```

## Tools to Use

- `Read`: Read script files
- `Write`: Create new scripts
- `Edit`: Modify existing scripts
- `Bash`: Execute and test scripts
- `Grep`: Search patterns and analyze code
- `Glob`: Find script files

### Common Commands

```bash
# WHY: Test script syntax without execution
bash -n script.sh

# WHY: Run with debug output
bash -x script.sh

# WHY: Check for common issues with shellcheck
shellcheck script.sh

# WHY: Make script executable
chmod +x script.sh

# WHY: Find all shell scripts in a project
find . -name "*.sh" -type f
```

## Workflow

1. **Requirements Analysis**: Clarify script purpose and requirements
2. **Structure Planning**: Design necessary functions, variables, and error handling
3. **Implementation**: Write code following best practices
4. **Error Handling**: Add error case handling
5. **Testing**: Test with various scenarios
6. **Validation**: Validate with tools like shellcheck
7. **Documentation**: Document usage and options
8. **Security Review**: Check for security risks

## Related Skills

This skill relates to:

- System administration and DevOps tasks
- Build and deployment automation
- Environment setup and configuration
- CLI tool development

## Reference Documentation

Detailed reference documentation:

- [Bash Features](references/bash-features.md) - Bash-specific features and syntax
- [Zsh Features](references/zsh-features.md) - Zsh-specific features and extensions
- [Security Best Practices](references/security-best-practices.md) - Security guidelines
- [Common Patterns](references/common-patterns.md) - Practical pattern collection

## Key Reminders

- Always enable error handling with `set -euo pipefail`
- Quote all variable expansions
- Always validate and sanitize user input
- Avoid using `eval`
- Output error messages to stderr
- Create temporary files with `mktemp`
- Use `local` within functions to limit scope
- Maintain POSIX compatibility or specify shell explicitly in shebang
- Validate scripts with shellcheck
- Comments should explain "WHY"
