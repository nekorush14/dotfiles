# Shell Script Security Best Practices

Comprehensive security guidelines for writing secure shell scripts, preventing common vulnerabilities, and protecting against attacks.

## Table of Contents

- [Input Validation](#input-validation)
- [Command Injection Prevention](#command-injection-prevention)
- [File Operations Security](#file-operations-security)
- [Environment Security](#environment-security)
- [Credential Management](#credential-management)
- [Privilege Management](#privilege-management)
- [Temporary File Handling](#temporary-file-handling)
- [Network Security](#network-security)
- [Logging and Auditing](#logging-and-auditing)
- [Common Vulnerabilities](#common-vulnerabilities)

## Input Validation

Always validate and sanitize user input:

```bash
# WHY: Validate input format
validate_email() {
  local email="$1"
  if [[ ! "$email" =~ ^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$ ]]; then
    echo "Error: Invalid email format" >&2
    return 1
  fi
  return 0
}

# WHY: Validate numeric input
validate_port() {
  local port="$1"
  if [[ ! "$port" =~ ^[0-9]+$ ]] || ((port < 1 || port > 65535)); then
    echo "Error: Invalid port number" >&2
    return 1
  fi
  return 0
}

# WHY: Whitelist allowed values
validate_action() {
  local action="$1"
  case "$action" in
    start|stop|restart|status)
      return 0
      ;;
    *)
      echo "Error: Invalid action: $action" >&2
      return 1
      ;;
  esac
}

# WHY: Sanitize filename input
sanitize_filename() {
  local filename="$1"
  # WHY: Remove path separators and dangerous characters
  filename="${filename//[\/\\:*?\"<>|]/}"
  # WHY: Remove leading dots (hidden files)
  filename="${filename#.}"
  # WHY: Limit to safe characters
  filename="${filename//[^a-zA-Z0-9._-]/}"
  echo "$filename"
}

# WHY: Validate path is within expected directory
validate_path() {
  local input_path="$1"
  local base_dir="$2"

  # WHY: Resolve to absolute path
  local real_path
  real_path=$(realpath -m "$input_path" 2>/dev/null) || return 1

  # WHY: Check if path is under base directory
  if [[ "$real_path" != "$base_dir"* ]]; then
    echo "Error: Path outside allowed directory" >&2
    return 1
  fi

  echo "$real_path"
}
```

## Command Injection Prevention

Prevent command injection vulnerabilities:

```bash
# WHY: NEVER use eval with user input
# DANGEROUS:
# eval "$user_input"

# WHY: NEVER use dynamic command construction
# DANGEROUS:
# cmd="ls $user_input"
# $cmd

# WHY: Always use arrays for commands with arguments
# SAFE:
files=()
while IFS= read -r -d '' file; do
  files+=("$file")
done < <(find "$search_dir" -name "*.txt" -print0)

rm -f "${files[@]}"

# WHY: Quote all variable expansions
# SAFE:
grep "$pattern" "$file"
# DANGEROUS:
# grep $pattern $file  # Can be exploited with pattern="-e dangerous"

# WHY: Use -- to separate options from arguments
rm -f -- "$file"
grep -r -- "$pattern" .

# WHY: Validate before using in commands
safe_copy() {
  local src="$1"
  local dst="$2"

  # WHY: Validate inputs
  if [[ ! -f "$src" ]]; then
    echo "Error: Source file does not exist" >&2
    return 1
  fi

  if [[ "$dst" == /* ]]; then
    echo "Error: Absolute paths not allowed" >&2
    return 1
  fi

  # WHY: Use quoted variables
  cp -f -- "$src" "$dst"
}

# WHY: Use printf instead of echo for untrusted input
# SAFE:
printf '%s\n' "$user_input"
# DANGEROUS:
# echo "$user_input"  # Can interpret escape sequences
```

## File Operations Security

Secure file operations:

```bash
# WHY: Check file permissions before reading sensitive data
check_file_secure() {
  local file="$1"

  # WHY: File must exist and be a regular file
  if [[ ! -f "$file" ]]; then
    echo "Error: Not a regular file: $file" >&2
    return 1
  fi

  # WHY: Check ownership
  local file_owner
  file_owner=$(stat -c '%U' "$file" 2>/dev/null) || return 1

  if [[ "$file_owner" != "$USER" && "$file_owner" != "root" ]]; then
    echo "Error: File owned by untrusted user: $file_owner" >&2
    return 1
  fi

  # WHY: Check permissions (should not be world-writable)
  local perms
  perms=$(stat -c '%a' "$file" 2>/dev/null) || return 1

  if [[ "${perms: -1}" =~ [2367] ]]; then
    echo "Error: File is world-writable: $file" >&2
    return 1
  fi

  return 0
}

# WHY: Create files with secure permissions
create_secure_file() {
  local file="$1"

  # WHY: Set umask to create with restricted permissions
  local old_umask
  old_umask=$(umask)
  umask 077  # rw------- (600)

  # WHY: Create file
  touch "$file" || {
    umask "$old_umask"
    return 1
  }

  umask "$old_umask"
  return 0
}

# WHY: Prevent symlink attacks
safe_write() {
  local file="$1"
  local content="$2"

  # WHY: Check if path contains symlinks
  if [[ -L "$file" ]]; then
    echo "Error: Will not write to symlink: $file" >&2
    return 1
  fi

  # WHY: Check parent directory for symlinks
  local dir
  dir=$(dirname "$file")
  if [[ -L "$dir" ]]; then
    echo "Error: Parent directory is symlink: $dir" >&2
    return 1
  fi

  # WHY: Write with restricted permissions
  (umask 077 && printf '%s\n' "$content" > "$file")
}

# WHY: Safely check file existence without following symlinks
if [[ -e "$file" && ! -L "$file" ]]; then
  echo "Regular file exists"
fi
```

## Environment Security

Secure environment handling:

```bash
# WHY: Clean environment for subprocesses
run_sandboxed() {
  local command="$1"
  shift

  # WHY: Start with minimal environment
  env -i \
    HOME="$HOME" \
    USER="$USER" \
    PATH="/usr/local/bin:/usr/bin:/bin" \
    "$command" "$@"
}

# WHY: Validate PATH
validate_path_env() {
  # WHY: Check for current directory in PATH (security risk)
  if [[ ":$PATH:" == *"::"* ]] || [[ ":$PATH:" == *":.:*" ]]; then
    echo "Error: Current directory in PATH" >&2
    return 1
  fi

  # WHY: Check for writable directories in PATH
  local dir
  IFS=':' read -ra dirs <<< "$PATH"
  for dir in "${dirs[@]}"; do
    if [[ -w "$dir" ]]; then
      echo "Warning: Writable directory in PATH: $dir" >&2
    fi
  done
}

# WHY: Use absolute paths for commands in production
# SAFE:
/usr/bin/git status
# RISKY:
# git status  # Subject to PATH manipulation

# WHY: Unset sensitive variables before exec
unset PASSWORD
unset API_KEY
exec "$@"
```

## Credential Management

Handle credentials securely:

```bash
# WHY: Never hardcode credentials
# DANGEROUS:
# password="secret123"

# WHY: Read from secure sources
read_password() {
  local password

  # WHY: Use silent read for password input
  read -s -p "Enter password: " password
  echo >&2  # Newline after password input

  # WHY: Validate password is not empty
  if [[ -z "$password" ]]; then
    echo "Error: Password cannot be empty" >&2
    return 1
  fi

  echo "$password"
}

# WHY: Store credentials securely
store_credentials() {
  local creds_file="$1"
  local password="$2"

  # WHY: Create with restricted permissions
  (umask 077 && printf '%s\n' "$password" > "$creds_file")

  # WHY: Verify permissions
  chmod 600 "$creds_file"
}

# WHY: Never log credentials
log_command() {
  local cmd="$1"

  # WHY: Redact sensitive parameters
  cmd="${cmd//--password=*/--password=***}"
  cmd="${cmd//--token=*/--token=***}"

  echo "Executing: $cmd" >> /var/log/script.log
}

# WHY: Clear credentials from memory when done
cleanup_credentials() {
  # WHY: Overwrite variables
  password="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
  unset password

  # WHY: Remove credential files
  if [[ -f "$temp_creds" ]]; then
    shred -u "$temp_creds" 2>/dev/null || rm -f "$temp_creds"
  fi
}
```

## Privilege Management

Handle privileges carefully:

```bash
# WHY: Check if running as root
if [[ $EUID -eq 0 ]]; then
  echo "Error: Do not run this script as root" >&2
  exit 1
fi

# WHY: Drop privileges when possible
drop_privileges() {
  local target_user="$1"

  if [[ $EUID -eq 0 ]]; then
    # WHY: Switch to non-privileged user
    exec su -s /bin/bash "$target_user" -c "$0 $*"
  fi
}

# WHY: Request sudo only when needed
run_privileged() {
  local command="$1"
  shift

  # WHY: Prompt for sudo
  if ! sudo -n true 2>/dev/null; then
    echo "This operation requires sudo privileges"
    sudo -v || return 1
  fi

  # WHY: Run specific command with sudo
  sudo "$command" "$@"
}

# WHY: Validate sudo permissions
check_sudo() {
  if ! sudo -n true 2>/dev/null; then
    echo "Error: This script requires sudo access" >&2
    exit 1
  fi
}
```

## Temporary File Handling

Create and manage temporary files securely:

```bash
# WHY: Always use mktemp
temp_file=$(mktemp) || {
  echo "Error: Failed to create temp file" >&2
  exit 1
}

# WHY: Set trap to cleanup temp files
cleanup() {
  local exit_code=$?
  # WHY: Remove temp files on exit
  rm -f "$temp_file" "$temp_dir"/*.tmp 2>/dev/null
  exit "$exit_code"
}
trap cleanup EXIT ERR INT TERM

# WHY: Create temporary directory
temp_dir=$(mktemp -d) || {
  echo "Error: Failed to create temp directory" >&2
  exit 1
}

# WHY: Set restrictive permissions on temp directory
chmod 700 "$temp_dir"

# WHY: Use temp directory in TMPDIR
export TMPDIR="$temp_dir"

# WHY: Predictable temp file names are dangerous
# DANGEROUS:
# temp_file="/tmp/myapp-$$"  # Can be predicted and attacked

# WHY: Write sensitive data to temp files securely
secure_temp() {
  local content="$1"

  local temp_file
  temp_file=$(mktemp)

  # WHY: Set restrictive permissions
  chmod 600 "$temp_file"

  # WHY: Write data
  printf '%s\n' "$content" > "$temp_file"

  echo "$temp_file"
}
```

## Network Security

Secure network operations:

```bash
# WHY: Validate URLs before fetching
validate_url() {
  local url="$1"

  # WHY: Check protocol
  if [[ ! "$url" =~ ^https?:// ]]; then
    echo "Error: Only HTTP/HTTPS URLs allowed" >&2
    return 1
  fi

  # WHY: Validate hostname
  if [[ "$url" =~ @|localhost|127\.|0\.0\.0\.0 ]]; then
    echo "Error: Suspicious URL detected" >&2
    return 1
  fi

  return 0
}

# WHY: Download files securely
safe_download() {
  local url="$1"
  local output="$2"

  # WHY: Validate URL
  validate_url "$url" || return 1

  # WHY: Use secure options
  curl \
    --silent \
    --show-error \
    --fail \
    --location \
    --max-redirs 3 \
    --max-time 30 \
    --output "$output" \
    -- "$url"
}

# WHY: Verify checksums after download
verify_download() {
  local file="$1"
  local expected_checksum="$2"

  local actual_checksum
  actual_checksum=$(sha256sum "$file" | cut -d' ' -f1)

  if [[ "$actual_checksum" != "$expected_checksum" ]]; then
    echo "Error: Checksum mismatch" >&2
    rm -f "$file"
    return 1
  fi

  return 0
}
```

## Logging and Auditing

Implement secure logging:

```bash
# WHY: Log to secure location
LOG_FILE="/var/log/secure/script.log"

# WHY: Ensure log directory exists with proper permissions
init_logging() {
  local log_dir
  log_dir=$(dirname "$LOG_FILE")

  if [[ ! -d "$log_dir" ]]; then
    mkdir -p "$log_dir"
    chmod 750 "$log_dir"
  fi

  # WHY: Create log file with restricted permissions
  if [[ ! -f "$LOG_FILE" ]]; then
    touch "$LOG_FILE"
    chmod 640 "$LOG_FILE"
  fi
}

# WHY: Log with timestamp and level
log_message() {
  local level="$1"
  shift
  local message="$*"

  # WHY: Add timestamp
  local timestamp
  timestamp=$(date '+%Y-%m-%d %H:%M:%S')

  # WHY: Sanitize message (remove control characters)
  message="${message//[$'\r\n\t']/ }"

  # WHY: Write to log
  printf '[%s] [%s] %s\n' "$timestamp" "$level" "$message" >> "$LOG_FILE"
}

# WHY: Log security events
log_security_event() {
  local event="$1"
  log_message "SECURITY" "$event"

  # WHY: Also log to syslog if available
  if command -v logger &> /dev/null; then
    logger -t "$(basename "$0")" -p auth.warning "SECURITY: $event"
  fi
}

# WHY: Audit script execution
audit_execution() {
  log_security_event "Script started by user: $USER (PID: $$)"
  log_security_event "Arguments: $*"
}
```

## Common Vulnerabilities

### Race Conditions

```bash
# WHY: Avoid TOCTOU (Time-of-Check-Time-of-Use) vulnerabilities

# DANGEROUS: Race condition
if [[ -f "$file" ]]; then
  # WHY: File could be replaced between check and use
  process_file "$file"
fi

# SAFE: Open file atomically
if exec 3< "$file" 2>/dev/null; then
  # WHY: File is opened and locked
  process_file <&3
  exec 3<&-
fi
```

### Shell Expansion Attacks

```bash
# WHY: Be careful with unquoted wildcards

# DANGEROUS:
# files=$(ls *.txt)  # Can be exploited with files named '-la'

# SAFE:
files=(*.txt)
if [[ ${#files[@]} -gt 0 && -e "${files[0]}" ]]; then
  for file in "${files[@]}"; do
    process_file "$file"
  done
fi
```

### Directory Traversal

```bash
# WHY: Prevent directory traversal attacks

# DANGEROUS:
# cat "uploads/$user_file"  # user_file could be "../../../etc/passwd"

# SAFE:
safe_read() {
  local base_dir="/var/uploads"
  local user_file="$1"

  # WHY: Remove path separators from user input
  user_file="${user_file//[\/\\]/}"

  # WHY: Construct full path
  local full_path="$base_dir/$user_file"

  # WHY: Resolve to absolute path
  full_path=$(realpath "$full_path" 2>/dev/null) || return 1

  # WHY: Verify path is under base directory
  if [[ "$full_path" != "$base_dir"* ]]; then
    echo "Error: Path traversal attempt detected" >&2
    return 1
  fi

  cat "$full_path"
}
```

## Security Checklist

- [ ] All user input is validated and sanitized
- [ ] No use of `eval` with untrusted data
- [ ] All variables are properly quoted
- [ ] File operations use secure permissions (600/700)
- [ ] Temporary files created with `mktemp`
- [ ] Credentials not hardcoded or logged
- [ ] Absolute paths used for commands in production
- [ ] PATH environment validated
- [ ] Symlink attacks prevented
- [ ] Race conditions addressed
- [ ] Error messages don't leak sensitive information
- [ ] Cleanup handlers registered with `trap`
- [ ] Security events logged and audited
- [ ] Privileges dropped when possible
- [ ] Network operations validated and restricted

## Key Reminders

- Never trust user input - always validate
- Quote all variable expansions
- Avoid `eval` and dynamic command construction
- Use `mktemp` for temporary files
- Set `set -euo pipefail` for error handling
- Implement proper cleanup with trap handlers
- Log security events
- Use absolute paths for critical commands
- Check file permissions before operating on sensitive files
- Document security assumptions in comments
