# Bash-Specific Features

Comprehensive guide to Bash-specific features and syntax that extend beyond POSIX shell capabilities.

## Table of Contents

- [Arrays](#arrays)
- [Associative Arrays](#associative-arrays)
- [Extended Pattern Matching](#extended-pattern-matching)
- [Process Substitution](#process-substitution)
- [Command Substitution](#command-substitution)
- [Here Strings](#here-strings)
- [Brace Expansion](#brace-expansion)
- [Arithmetic Operations](#arithmetic-operations)
- [String Manipulation](#string-manipulation)
- [Control Structures](#control-structures)
- [Function Features](#function-features)
- [Built-in Commands](#built-in-commands)

## Arrays

Bash supports indexed arrays (Bash 2.0+) and associative arrays (Bash 4.0+).

### Indexed Arrays

```bash
# WHY: Declare array explicitly for clarity
declare -a fruits
fruits=("apple" "banana" "cherry")

# WHY: Alternative initialization syntax
colors=(red green blue)

# WHY: Access individual elements (0-indexed)
echo "${fruits[0]}"  # apple

# WHY: Access all elements
echo "${fruits[@]}"  # apple banana cherry
echo "${fruits[*]}"  # apple banana cherry (joins with IFS)

# WHY: Get array length
echo "${#fruits[@]}"  # 3

# WHY: Append to array
fruits+=("date" "elderberry")

# WHY: Iterate over array
for fruit in "${fruits[@]}"; do
  echo "$fruit"
done

# WHY: Access array indices
echo "${!fruits[@]}"  # 0 1 2 3 4

# WHY: Array slicing (start:length)
echo "${fruits[@]:1:2}"  # banana cherry

# WHY: Remove element by index
unset 'fruits[1]'

# WHY: Read lines into array
mapfile -t lines < file.txt
# or
readarray -t lines < file.txt
```

## Associative Arrays

```bash
# WHY: Must declare associative arrays explicitly (Bash 4+)
declare -A user_data
user_data=(
  [name]="John Doe"
  [email]="john@example.com"
  [age]="30"
)

# WHY: Alternative assignment
declare -A config
config[host]="localhost"
config[port]="8080"

# WHY: Access values by key
echo "${user_data[name]}"  # John Doe

# WHY: Check if key exists
if [[ -v user_data[email] ]]; then
  echo "Email: ${user_data[email]}"
fi

# WHY: Get all keys
echo "${!user_data[@]}"  # name email age

# WHY: Get all values
echo "${user_data[@]}"  # John Doe john@example.com 30

# WHY: Iterate over keys and values
for key in "${!config[@]}"; do
  echo "$key: ${config[$key]}"
done
```

## Extended Pattern Matching

Enable with `shopt -s extglob`:

```bash
# WHY: Enable extended globbing patterns
shopt -s extglob

# WHY: Pattern matching operators
# ?(pattern)  - Matches zero or one occurrence
# *(pattern)  - Matches zero or more occurrences
# +(pattern)  - Matches one or more occurrences
# @(pattern)  - Matches exactly one occurrence
# !(pattern)  - Matches anything except the pattern

# Examples:
# WHY: Match files with specific extensions
ls *.@(jpg|png|gif)

# WHY: Match files NOT ending with .txt
ls !(*.txt)

# WHY: Remove specific extensions from string
filename="document.backup.txt"
echo "${filename%.@(txt|bak|tmp)}"

# WHY: Use in case statements
case "$file" in
  *.@(jpg|jpeg|png))
    echo "Image file"
    ;;
  *.@(mp3|wav|flac))
    echo "Audio file"
    ;;
esac
```

## Process Substitution

```bash
# WHY: Use process output as a file
diff <(sort file1.txt) <(sort file2.txt)

# WHY: Compare command outputs
diff <(ls dir1) <(ls dir2)

# WHY: Pass multiple inputs to a command
paste <(cut -d, -f1 data.csv) <(cut -d, -f3 data.csv)

# WHY: Read process output
while IFS= read -r line; do
  echo "Line: $line"
done < <(find . -name "*.txt")

# WHY: Output substitution (less common)
echo "output" > >(tee file1.txt file2.txt)
```

## Command Substitution

```bash
# WHY: Modern syntax (preferred)
current_date=$(date +%Y-%m-%d)
file_count=$(find . -type f | wc -l)

# WHY: Nested command substitution
result=$(echo "$(whoami) is logged in")

# WHY: Capture output and exit code
output=$(command 2>&1)
exit_code=$?

# WHY: Preserve trailing newlines
output=$(command; echo x)
output=${output%x}
```

## Here Strings

```bash
# WHY: Pass string directly to stdin
grep "pattern" <<< "$variable"

# WHY: Compare with here document
cat <<< "Single line input"

# WHY: Use with read
read -r first second <<< "hello world"
echo "$first"   # hello
echo "$second"  # world

# WHY: Pass multiline string
bc <<< "2 + 2"  # 4
```

## Brace Expansion

```bash
# WHY: Generate sequences
echo {1..10}        # 1 2 3 4 5 6 7 8 9 10
echo {a..z}         # a b c d ... z
echo {01..12}       # 01 02 03 ... 12 (zero-padded)

# WHY: Create multiple files/directories
mkdir -p project/{src,test,docs}
touch file{1..5}.txt

# WHY: Generate combinations
echo {a,b,c}{1,2,3}  # a1 a2 a3 b1 b2 b3 c1 c2 c3

# WHY: Backup files
cp file.txt{,.bak}  # Expands to: cp file.txt file.txt.bak

# WHY: Increment with step (Bash 4+)
echo {0..100..10}   # 0 10 20 30 ... 100

# WHY: Descending sequence
echo {10..1}        # 10 9 8 7 ... 1
```

## Arithmetic Operations

```bash
# WHY: Arithmetic expansion
result=$((2 + 2))
echo $((10 * 5))

# WHY: Increment/decrement
count=0
((count++))
((count += 5))
((count--))

# WHY: Arithmetic evaluation
if ((count > 10)); then
  echo "Count is greater than 10"
fi

# WHY: Various operators
echo $((10 / 3))     # 3 (integer division)
echo $((10 % 3))     # 1 (modulo)
echo $((2 ** 8))     # 256 (exponentiation)
echo $((~5))         # -6 (bitwise NOT)
echo $((5 & 3))      # 1 (bitwise AND)
echo $((5 | 3))      # 7 (bitwise OR)
echo $((5 ^ 3))      # 6 (bitwise XOR)

# WHY: Conditional operator
max=$((a > b ? a : b))

# WHY: Let command for arithmetic
let "result = 2 + 2"
let result++
```

## String Manipulation

```bash
# WHY: String length
string="hello world"
echo "${#string}"  # 11

# WHY: Substring extraction (offset:length)
echo "${string:0:5}"   # hello
echo "${string:6}"     # world
echo "${string: -5}"   # world (note space before -)

# WHY: Remove shortest match from beginning
filename="path/to/file.txt"
echo "${filename#*/}"      # to/file.txt

# WHY: Remove longest match from beginning
echo "${filename##*/}"     # file.txt

# WHY: Remove shortest match from end
echo "${filename%.*}"      # path/to/file

# WHY: Remove longest match from end
echo "${filename%%/*}"     # path

# WHY: Search and replace (first occurrence)
text="hello world hello"
echo "${text/hello/hi}"    # hi world hello

# WHY: Search and replace (all occurrences)
echo "${text//hello/hi}"   # hi world hi

# WHY: Replace at beginning
echo "${text/#hello/hi}"   # hi world hello

# WHY: Replace at end
echo "${text/%hello/hi}"   # hello world hi

# WHY: Case conversion (Bash 4+)
echo "${string^^}"         # HELLO WORLD (uppercase)
echo "${string,,}"         # hello world (lowercase)
echo "${string^}"          # Hello world (capitalize first)
echo "${string^^[hw]}"     # Hello World (uppercase specific chars)
```

## Control Structures

### Select Statement

```bash
# WHY: Create interactive menus
PS3="Select an option: "
options=("Option 1" "Option 2" "Option 3" "Quit")

select opt in "${options[@]}"; do
  case $REPLY in
    1)
      echo "You selected Option 1"
      ;;
    2)
      echo "You selected Option 2"
      ;;
    3)
      echo "You selected Option 3"
      ;;
    4)
      echo "Goodbye"
      break
      ;;
    *)
      echo "Invalid option"
      ;;
  esac
done
```

### Until Loop

```bash
# WHY: Loop until condition is true
count=0
until ((count >= 5)); do
  echo "Count: $count"
  ((count++))
done
```

### C-style For Loop

```bash
# WHY: Traditional for loop syntax
for ((i = 0; i < 10; i++)); do
  echo "Iteration: $i"
done
```

## Function Features

```bash
# WHY: Return values (0-255)
get_status() {
  # Do some work
  return 0  # Success
}

# WHY: Return strings via stdout
get_value() {
  echo "return value"
}
result=$(get_value)

# WHY: Local variables
process_data() {
  local input="$1"
  local output="processed: $input"
  echo "$output"
}

# WHY: Function with named arguments (using local)
create_user() {
  local username="$1"
  local email="$2"
  local age="${3:-0}"  # Default value

  echo "Creating user: $username ($email), age: $age"
}

# WHY: Export functions to subshells
export -f my_function
bash -c 'my_function'
```

## Built-in Commands

### Read Command

```bash
# WHY: Read input with timeout
read -t 5 -p "Enter name (5 sec timeout): " name

# WHY: Read without trailing newline removal
IFS= read -r line

# WHY: Read into array
IFS=',' read -ra fields <<< "a,b,c,d"

# WHY: Read single character
read -n 1 -p "Press any key to continue..."

# WHY: Silent read (for passwords)
read -s -p "Enter password: " password
echo
```

### Declare/Typeset

```bash
# WHY: Declare variable attributes
declare -r CONSTANT="value"    # Read-only
declare -i number=42           # Integer
declare -l lowercase="HELLO"   # Convert to lowercase
declare -u uppercase="hello"   # Convert to uppercase
declare -x EXPORTED="value"    # Export variable

# WHY: List all functions
declare -F

# WHY: List function definition
declare -f function_name
```

### Test/[[]] Enhancements

```bash
# WHY: Pattern matching in [[ ]]
if [[ "$string" == pattern* ]]; then
  echo "Matches pattern"
fi

# WHY: Regex matching
if [[ "$email" =~ ^[a-z]+@[a-z]+\.[a-z]+$ ]]; then
  echo "Valid email format"
fi

# WHY: Logical operators
if [[ "$a" -gt 5 && "$b" -lt 10 ]]; then
  echo "Condition met"
fi

if [[ "$x" == "foo" || "$x" == "bar" ]]; then
  echo "x is foo or bar"
fi
```

### Printf

```bash
# WHY: Formatted output (more powerful than echo)
printf "Name: %s, Age: %d\n" "John" 30
printf "%.2f\n" 3.14159  # 3.14
printf "%10s\n" "right"   # Right-aligned
printf "%-10s\n" "left"   # Left-aligned
printf "%x\n" 255         # ff (hexadecimal)
```

### Mapfile/Readarray

```bash
# WHY: Read file into array efficiently
mapfile -t lines < file.txt

# WHY: Skip first N lines
mapfile -t -s 5 lines < file.txt

# WHY: Read only N lines
mapfile -t -n 10 lines < file.txt

# WHY: Process each line with callback
callback() {
  echo "Processing: $1"
}
mapfile -t -C callback lines < file.txt
```

## Key Reminders

- Use Bash-specific features only when targeting Bash explicitly
- Check Bash version requirements (especially for Bash 4+ features)
- Consider POSIX alternatives for maximum portability
- Use `shopt` to enable optional Bash features
- Test Bash-specific scripts with the specific Bash version in production
- Document Bash version requirements in script headers
