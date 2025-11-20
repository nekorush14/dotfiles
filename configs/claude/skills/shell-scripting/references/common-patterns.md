# Common Shell Scripting Patterns

Practical collection of commonly used shell scripting patterns and idioms for everyday tasks.

## Table of Contents

- [Script Template](#script-template)
- [Configuration Management](#configuration-management)
- [Logging Patterns](#logging-patterns)
- [Error Handling Patterns](#error-handling-patterns)
- [Progress Indicators](#progress-indicators)
- [File Processing](#file-processing)
- [Data Validation](#data-validation)
- [Parallel Execution](#parallel-execution)
- [Retry Logic](#retry-logic)
- [Lock Files](#lock-files)
- [Signal Handling](#signal-handling)

## Script Template

Complete template for production scripts:

```bash
#!/usr/bin/env bash
#
# Script Name: script-name.sh
# Description: Brief description of what this script does
# Author: Your Name
# Version: 1.0.0
# Usage: script-name.sh [OPTIONS] [ARGUMENTS]
#

set -euo pipefail

# WHY: Set script directory for relative paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly SCRIPT_DIR

# WHY: Define constants
readonly SCRIPT_NAME="$(basename "$0")"
readonly VERSION="1.0.0"

# WHY: Default configuration
DEBUG="${DEBUG:-false}"
VERBOSE="${VERBOSE:-false}"

# WHY: Cleanup handler
cleanup() {
  local exit_code=$?

  # WHY: Perform cleanup operations
  [[ -f "$temp_file" ]] && rm -f "$temp_file"

  # WHY: Log exit status
  if [[ $exit_code -ne 0 ]]; then
    log_error "Script failed with exit code: $exit_code"
  fi

  exit "$exit_code"
}
trap cleanup EXIT ERR INT TERM

# WHY: Logging functions
log_info() {
  echo "[INFO] $*"
}

log_error() {
  echo "[ERROR] $*" >&2
}

log_debug() {
  if [[ "$DEBUG" == true ]]; then
    echo "[DEBUG] $*" >&2
  fi
}

# WHY: Usage information
usage() {
  cat << EOF
Usage: $SCRIPT_NAME [OPTIONS] [ARGUMENTS]

Description of the script.

Options:
  -h, --help       Show this help message
  -v, --verbose    Enable verbose output
  -d, --debug      Enable debug mode
  -V, --version    Show version information

Examples:
  $SCRIPT_NAME --verbose input.txt
  $SCRIPT_NAME -d file1.txt file2.txt

EOF
}

# WHY: Version information
version() {
  echo "$SCRIPT_NAME version $VERSION"
}

# WHY: Main function
main() {
  local verbose=false
  local debug=false

  # WHY: Parse arguments
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
      -d|--debug)
        debug=true
        shift
        ;;
      -V|--version)
        version
        exit 0
        ;;
      -*)
        log_error "Unknown option: $1"
        usage >&2
        exit 1
        ;;
      *)
        break
        ;;
    esac
  done

  # WHY: Set global flags
  VERBOSE="$verbose"
  DEBUG="$debug"

  # WHY: Validate required arguments
  if [[ $# -eq 0 ]]; then
    log_error "Missing required arguments"
    usage >&2
    exit 1
  fi

  # WHY: Main script logic here
  log_info "Starting script..."

  # Implementation...

  log_info "Script completed successfully"
}

# WHY: Run main function
main "$@"
```

## Configuration Management

Load and manage configuration:

```bash
# WHY: Load configuration from file
load_config() {
  local config_file="$1"

  # WHY: Check if config exists
  if [[ ! -f "$config_file" ]]; then
    log_error "Config file not found: $config_file"
    return 1
  fi

  # WHY: Source config safely
  # shellcheck source=/dev/null
  source "$config_file" || {
    log_error "Failed to load config: $config_file"
    return 1
  }
}

# WHY: Load config with defaults
load_config_with_defaults() {
  local config_file="${1:-$HOME/.config/app/config.sh}"

  # WHY: Set defaults
  APP_HOST="${APP_HOST:-localhost}"
  APP_PORT="${APP_PORT:-8080}"
  APP_DEBUG="${APP_DEBUG:-false}"

  # WHY: Override with config file if exists
  if [[ -f "$config_file" ]]; then
    log_debug "Loading config from: $config_file"
    load_config "$config_file"
  else
    log_debug "Using default configuration"
  fi

  # WHY: Validate required settings
  : "${APP_HOST:?Error: APP_HOST must be set}"
  : "${APP_PORT:?Error: APP_PORT must be set}"
}

# WHY: Parse INI-style config
parse_ini() {
  local config_file="$1"
  local section="${2:-}"

  awk -F= -v section="$section" '
    /^\[.*\]$/ {
      current_section = substr($0, 2, length($0)-2)
      next
    }
    /^[^#;]/ {
      if (section == "" || current_section == section) {
        key = $1
        gsub(/^[ \t]+|[ \t]+$/, "", key)
        value = substr($0, index($0, "=") + 1)
        gsub(/^[ \t]+|[ \t]+$/, "", value)
        print key "=" value
      }
    }
  ' "$config_file"
}
```

## Logging Patterns

Advanced logging implementations:

```bash
# WHY: Structured logging with levels
declare -A LOG_LEVELS=(
  [DEBUG]=0
  [INFO]=1
  [WARN]=2
  [ERROR]=3
)

LOG_LEVEL="${LOG_LEVEL:-INFO}"

log() {
  local level="$1"
  shift
  local message="$*"

  # WHY: Check if level should be logged
  if [[ ${LOG_LEVELS[$level]:-0} -lt ${LOG_LEVELS[$LOG_LEVEL]:-1} ]]; then
    return 0
  fi

  # WHY: Format log message
  local timestamp
  timestamp=$(date '+%Y-%m-%d %H:%M:%S')

  local output="[$timestamp] [$level] $message"

  # WHY: Output to appropriate stream
  case "$level" in
    ERROR|WARN)
      echo "$output" >&2
      ;;
    *)
      echo "$output"
      ;;
  esac

  # WHY: Also log to file if LOG_FILE is set
  if [[ -n "${LOG_FILE:-}" ]]; then
    echo "$output" >> "$LOG_FILE"
  fi
}

# WHY: Log with context
log_with_context() {
  local level="$1"
  local context="$2"
  shift 2
  local message="$*"

  log "$level" "[$context] $message"
}

# WHY: Convenience functions
log_debug() { log DEBUG "$@"; }
log_info() { log INFO "$@"; }
log_warn() { log WARN "$@"; }
log_error() { log ERROR "$@"; }
```

## Error Handling Patterns

Robust error handling:

```bash
# WHY: Die function for fatal errors
die() {
  log_error "$@"
  exit 1
}

# WHY: Require command to be available
require_command() {
  local cmd="$1"
  if ! command -v "$cmd" &> /dev/null; then
    die "Required command not found: $cmd"
  fi
}

# WHY: Assert condition
assert() {
  local condition="$1"
  local message="${2:-Assertion failed}"

  if ! eval "$condition"; then
    die "$message"
  fi
}

# WHY: Try/catch pattern
try() {
  local exit_code=0
  "$@" || exit_code=$?
  return $exit_code
}

handle_error() {
  local exit_code=$1
  local line_number=$2
  local command="$3"

  log_error "Command failed with exit code $exit_code at line $line_number: $command"
}

# WHY: Set up error handler
set -E
trap 'handle_error $? $LINENO "$BASH_COMMAND"' ERR

# WHY: Wrapper function with error handling
safe_execute() {
  local description="$1"
  shift

  log_info "Executing: $description"

  if ! "$@"; then
    log_error "Failed: $description"
    return 1
  fi

  log_info "Completed: $description"
  return 0
}
```

## Progress Indicators

Show progress to users:

```bash
# WHY: Simple spinner
spinner() {
  local pid=$1
  local message="${2:-Processing}"
  local spin='⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏'

  local i=0
  while kill -0 "$pid" 2>/dev/null; do
    i=$(((i + 1) % 10))
    printf '\r%s %s' "${spin:$i:1}" "$message"
    sleep 0.1
  done

  printf '\r\033[K'  # Clear line
}

# Usage:
# long_running_command &
# spinner $! "Loading data"

# WHY: Progress bar
progress_bar() {
  local current=$1
  local total=$2
  local width=50

  local percentage=$((current * 100 / total))
  local filled=$((current * width / total))
  local empty=$((width - filled))

  printf '\r['
  printf '%*s' "$filled" '' | tr ' ' '='
  printf '%*s' "$empty" ''
  printf '] %3d%%' "$percentage"

  if [[ $current -eq $total ]]; then
    echo
  fi
}

# Usage:
# for ((i=1; i<=100; i++)); do
#   progress_bar $i 100
#   sleep 0.05
# done

# WHY: Processing indicator with ETA
process_with_eta() {
  local total=$1
  local start_time
  start_time=$(date +%s)

  for ((i=1; i<=total; i++)); do
    # Do work here
    sleep 0.1

    # WHY: Calculate ETA
    local current_time
    current_time=$(date +%s)
    local elapsed=$((current_time - start_time))
    local rate=$((i * 100 / elapsed))
    local remaining=$((total - i))
    local eta=$((remaining * 100 / rate))

    printf '\rProcessing: %d/%d (ETA: %ds)' "$i" "$total" "$eta"
  done

  echo
}
```

## File Processing

Common file processing patterns:

```bash
# WHY: Process file line by line
process_file_lines() {
  local file="$1"

  while IFS= read -r line; do
    # WHY: Skip empty lines
    [[ -z "$line" ]] && continue

    # WHY: Skip comments
    [[ "$line" =~ ^# ]] && continue

    # Process line
    echo "Processing: $line"
  done < "$file"
}

# WHY: Process CSV file
process_csv() {
  local file="$1"
  local delimiter="${2:-,}"

  local line_num=0
  while IFS="$delimiter" read -ra fields; do
    ((line_num++))

    # WHY: Skip header
    if [[ $line_num -eq 1 ]]; then
      continue
    fi

    # Process fields
    echo "Field 1: ${fields[0]}"
    echo "Field 2: ${fields[1]}"
  done < "$file"
}

# WHY: Find and process files
find_and_process() {
  local search_dir="$1"
  local pattern="$2"

  # WHY: Use null-terminated output for safety
  while IFS= read -r -d '' file; do
    log_info "Processing: $file"

    # Process file
    process_file "$file"
  done < <(find "$search_dir" -name "$pattern" -type f -print0)
}

# WHY: Batch process files
batch_process() {
  local -a files=("$@")
  local batch_size=10
  local count=0

  for file in "${files[@]}"; do
    process_file "$file" &

    ((count++))

    # WHY: Limit concurrent processes
    if ((count % batch_size == 0)); then
      wait  # Wait for batch to complete
    fi
  done

  wait  # Wait for remaining processes
}
```

## Data Validation

Validation patterns:

```bash
# WHY: Validate required environment variables
validate_env() {
  local -a required_vars=("$@")

  for var in "${required_vars[@]}"; do
    if [[ -z "${!var:-}" ]]; then
      die "Required environment variable not set: $var"
    fi
  done
}

# Usage:
# validate_env DATABASE_URL API_KEY

# WHY: Validate file exists and is readable
validate_file() {
  local file="$1"

  if [[ ! -f "$file" ]]; then
    die "File not found: $file"
  fi

  if [[ ! -r "$file" ]]; then
    die "File not readable: $file"
  fi
}

# WHY: Validate directory exists and is writable
validate_directory() {
  local dir="$1"

  if [[ ! -d "$dir" ]]; then
    die "Directory not found: $dir"
  fi

  if [[ ! -w "$dir" ]]; then
    die "Directory not writable: $dir"
  fi
}

# WHY: Validate number range
validate_range() {
  local value="$1"
  local min="$2"
  local max="$3"

  if [[ ! "$value" =~ ^[0-9]+$ ]]; then
    die "Invalid number: $value"
  fi

  if ((value < min || value > max)); then
    die "Value out of range: $value (must be between $min and $max)"
  fi
}
```

## Parallel Execution

Execute tasks in parallel:

```bash
# WHY: Simple parallel execution with xargs
parallel_with_xargs() {
  local -a items=("$@")
  local max_jobs=4

  printf '%s\n' "${items[@]}" | \
    xargs -P "$max_jobs" -I {} bash -c 'process_item "{}"'
}

# WHY: Parallel execution with GNU parallel
parallel_with_gnu_parallel() {
  local -a items=("$@")

  # WHY: Check if GNU parallel is available
  require_command parallel

  printf '%s\n' "${items[@]}" | \
    parallel --jobs 4 --halt soon,fail=1 'process_item {}'
}

# WHY: Manual parallel execution
parallel_manual() {
  local -a items=("$@")
  local max_jobs=4
  local job_count=0

  for item in "${items[@]}"; do
    # WHY: Start background job
    process_item "$item" &

    ((job_count++))

    # WHY: Wait if max jobs reached
    if ((job_count >= max_jobs)); then
      wait -n  # Wait for any job to complete
      ((job_count--))
    fi
  done

  # WHY: Wait for remaining jobs
  wait
}
```

## Retry Logic

Implement retry mechanisms:

```bash
# WHY: Retry command with exponential backoff
retry_with_backoff() {
  local max_attempts="${1:-3}"
  local delay="${2:-1}"
  local max_delay="${3:-60}"
  shift 3
  local attempt=1

  while true; do
    if "$@"; then
      return 0
    fi

    if ((attempt >= max_attempts)); then
      log_error "Command failed after $max_attempts attempts"
      return 1
    fi

    log_warn "Attempt $attempt failed. Retrying in ${delay}s..."
    sleep "$delay"

    # WHY: Exponential backoff
    delay=$((delay * 2))
    if ((delay > max_delay)); then
      delay=$max_delay
    fi

    ((attempt++))
  done
}

# WHY: Retry with constant delay
retry() {
  local max_attempts="${1:-3}"
  local delay="${2:-5}"
  shift 2
  local attempt=1

  while ((attempt <= max_attempts)); do
    if "$@"; then
      return 0
    fi

    if ((attempt < max_attempts)); then
      log_warn "Attempt $attempt/$max_attempts failed. Retrying..."
      sleep "$delay"
    fi

    ((attempt++))
  done

  log_error "All $max_attempts attempts failed"
  return 1
}

# Usage:
# retry 3 5 curl -f https://example.com/api
# retry_with_backoff 5 1 30 some_command
```

## Lock Files

Prevent concurrent execution:

```bash
# WHY: Create lock file
acquire_lock() {
  local lock_file="${1:-/var/lock/$(basename "$0").lock}"
  local timeout="${2:-0}"

  local start_time
  start_time=$(date +%s)

  while true; do
    # WHY: Try to create lock file atomically
    if mkdir "$lock_file" 2>/dev/null; then
      # WHY: Store PID in lock file
      echo $$ > "$lock_file/pid"
      log_debug "Lock acquired: $lock_file"
      echo "$lock_file"
      return 0
    fi

    # WHY: Check if lock is stale
    if [[ -f "$lock_file/pid" ]]; then
      local pid
      pid=$(cat "$lock_file/pid")
      if ! kill -0 "$pid" 2>/dev/null; then
        log_warn "Removing stale lock (PID $pid no longer exists)"
        rm -rf "$lock_file"
        continue
      fi
    fi

    # WHY: Check timeout
    if ((timeout > 0)); then
      local current_time
      current_time=$(date +%s)
      local elapsed=$((current_time - start_time))

      if ((elapsed >= timeout)); then
        log_error "Failed to acquire lock after ${timeout}s"
        return 1
      fi

      log_info "Waiting for lock... (${elapsed}s/${timeout}s)"
      sleep 1
    else
      log_error "Lock file exists: $lock_file"
      return 1
    fi
  done
}

# WHY: Release lock file
release_lock() {
  local lock_file="$1"

  if [[ -d "$lock_file" ]]; then
    rm -rf "$lock_file"
    log_debug "Lock released: $lock_file"
  fi
}

# Usage:
# lock_file=$(acquire_lock "/var/lock/myapp.lock" 60) || exit 1
# trap "release_lock '$lock_file'" EXIT
```

## Signal Handling

Handle signals properly:

```bash
# WHY: Graceful shutdown handler
graceful_shutdown() {
  local signal="$1"

  log_info "Received $signal, shutting down gracefully..."

  # WHY: Stop background jobs
  if [[ -n "${worker_pid:-}" ]]; then
    kill -TERM "$worker_pid" 2>/dev/null
    wait "$worker_pid" 2>/dev/null
  fi

  # WHY: Cleanup resources
  cleanup

  # WHY: Exit with appropriate code
  exit $((128 + signal))
}

# WHY: Set up signal handlers
trap 'graceful_shutdown SIGINT' INT
trap 'graceful_shutdown SIGTERM' TERM
trap 'graceful_shutdown SIGHUP' HUP

# WHY: Ignore specific signals
trap '' SIGPIPE  # Ignore broken pipe

# WHY: Forward signal to child process
forward_signal() {
  local signal="$1"
  local child_pid="$2"

  if kill -0 "$child_pid" 2>/dev/null; then
    kill -"$signal" "$child_pid"
  fi
}
```

## Key Reminders

- Use these patterns as starting points, adapt to your needs
- Always validate inputs and handle errors
- Document complex patterns with WHY comments
- Test patterns thoroughly before production use
- Consider performance implications for large-scale operations
- Use shellcheck to validate script patterns
- Keep patterns simple and readable
- Consider POSIX compatibility when needed
