# Zsh-Specific Features

Comprehensive guide to Zsh-specific features and extensions that make it a powerful interactive shell and scripting language.

## Table of Contents

- [Arrays and Indexing](#arrays-and-indexing)
- [Associative Arrays](#associative-arrays)
- [Globbing Qualifiers](#globbing-qualifiers)
- [Extended Globbing](#extended-globbing)
- [Parameter Expansion Flags](#parameter-expansion-flags)
- [Prompt Expansion](#prompt-expansion)
- [Arithmetic and Math Functions](#arithmetic-and-math-functions)
- [Conditional Expressions](#conditional-expressions)
- [Modules and Built-ins](#modules-and-built-ins)
- [History Features](#history-features)
- [Completion System](#completion-system)

## Arrays and Indexing

Zsh arrays are 1-indexed by default (unlike Bash's 0-indexed arrays).

```bash
# WHY: Zsh arrays start at index 1 by default
fruits=(apple banana cherry)
echo "$fruits[1]"     # apple (not banana!)
echo "$fruits[2]"     # banana

# WHY: Access all elements
echo "$fruits[@]"     # apple banana cherry
echo "$fruits[*]"     # apple banana cherry

# WHY: Array length
echo "${#fruits}"     # 3

# WHY: Slice arrays (start,end inclusive)
echo "$fruits[1,2]"   # apple banana
echo "$fruits[2,-1]"  # banana cherry (negative indexing from end)

# WHY: Append to array
fruits+=(date elderberry)

# WHY: Prepend to array
fruits=(mango $fruits)

# WHY: Remove elements
fruits[2]=()          # Remove second element

# WHY: Reverse array
echo "${(Oa)fruits[@]}"  # Reverse order

# WHY: Join array with separator
echo "${(j:,:)fruits}"   # apple,banana,cherry

# WHY: Split string into array
IFS=',' read -rA fields <<< "a,b,c"
# or
fields=("${(@s:,:)string}")
```

## Associative Arrays

```bash
# WHY: Declare associative array
typeset -A config
config=(
  host localhost
  port 8080
  debug true
)

# WHY: Alternative assignment
config[timeout]=30

# WHY: Access values
echo "$config[host]"      # localhost

# WHY: Check if key exists
if (( ${+config[host]} )); then
  echo "Host is configured"
fi

# WHY: Get all keys
echo "${(@k)config}"      # host port debug timeout

# WHY: Get all values
echo "${(@v)config}"      # localhost 8080 true 30

# WHY: Iterate over key-value pairs
for key value in "${(@kv)config}"; do
  echo "$key: $value"
done

# WHY: Remove key
unset "config[debug]"
```

## Globbing Qualifiers

Zsh glob qualifiers provide powerful file filtering:

```bash
# WHY: Files only
ls *(.N)

# WHY: Directories only
ls *(/)

# WHY: Symbolic links only
ls *(@)

# WHY: Executable files
ls *(*)

# WHY: Files modified in last 24 hours
ls *(mh-24)

# WHY: Files modified more than 7 days ago
ls *(md+7)

# WHY: Files larger than 1MB
ls *(Lm+1)

# WHY: Files smaller than 100KB
ls *(Lk-100)

# WHY: Sort by modification time (newest first)
ls *(om)

# WHY: Sort by size (largest first)
ls *(OL)

# WHY: Limit to first 5 results
ls *(om[1,5])

# WHY: Get only basename
echo *(om[1]:t)

# WHY: Get only directory path
echo *(om[1]:h)

# WHY: Remove extension
echo *(om[1]:r)

# WHY: Get extension only
echo *(om[1]:e)

# WHY: Combine qualifiers (executable files modified today)
ls *(*mh-24)

# WHY: Recursive globbing with qualifiers
ls **/*.txt(.)        # Only files, not directories
```

## Extended Globbing

```bash
# WHY: Enable extended globbing (usually default in Zsh)
setopt EXTENDED_GLOB

# WHY: Exclude pattern with ^
ls ^*.txt             # All files except .txt

# WHY: Multiple exclusions
ls ^(*.txt|*.md)      # Exclude .txt and .md files

# WHY: Negate pattern with ~
ls *.txt~*backup*     # .txt files but not containing 'backup'

# WHY: Numeric ranges
ls file<1-10>.txt     # file1.txt through file10.txt

# WHY: Approximate matching (#a)
# Matches with minor differences (1 error allowed)
ls (#a1)exmple.txt    # Matches example.txt

# WHY: Case insensitive matching (#i)
ls (#i)readme*        # Matches README, readme, ReadMe, etc.

# WHY: Recursive globbing
ls **/*.js            # All .js files recursively
ls ***/*.js           # Follow symlinks while recursing
```

## Parameter Expansion Flags

Zsh provides powerful parameter expansion flags:

```bash
# WHY: Split string into words
string="one two three"
words=("${(@s/ /)string}")      # Split by space

# WHY: Join array with separator
array=(a b c)
echo "${(j:,:)array}"           # a,b,c

# WHY: Quote each element
echo "${(q)array[@]}"           # Properly quoted for eval

# WHY: Uppercase/lowercase
name="john doe"
echo "${(U)name}"               # JOHN DOE
echo "${(L)name}"               # john doe
echo "${(C)name}"               # John Doe (capitalize)

# WHY: Length of variable
echo "${(#)string}"             # Length in characters

# WHY: Sort array
numbers=(3 1 4 1 5 9)
echo "${(o)numbers[@]}"         # 1 1 3 4 5 9 (ascending)
echo "${(O)numbers[@]}"         # 9 5 4 3 1 1 (descending)

# WHY: Unique elements
echo "${(u)numbers[@]}"         # 1 3 4 5 9

# WHY: Reverse array
echo "${(Oa)array[@]}"          # Reverse order

# WHY: Padding
number=42
echo "${(l:5::0:)number}"       # 00042 (left pad)
echo "${(r:5::0:)number}"       # 42000 (right pad)

# WHY: Word splitting
setopt shwordsplit              # Enable word splitting (like bash)
unsetopt shwordsplit            # Disable (Zsh default)
```

## Prompt Expansion

```bash
# WHY: Current directory
PS1='%~ $ '

# WHY: Username and hostname
PS1='%n@%m %~ $ '

# WHY: Current time
PS1='%* %~ $ '                  # HH:MM:SS
PS1='%T %~ $ '                  # HH:MM

# WHY: Return status
PS1='%(?..%? )%~ $ '            # Show if non-zero

# WHY: Colors
PS1='%F{blue}%~%f $ '           # Blue directory
PS1='%F{green}%n%f@%F{red}%m%f $ '  # Colored parts

# WHY: Conditional expressions
PS1='%(?.%F{green}✓.%F{red}✗)%f %~ $ '  # Green ✓ or red ✗

# WHY: Git branch (requires vcs_info)
autoload -Uz vcs_info
precmd() { vcs_info }
setopt prompt_subst
PS1='${vcs_info_msg_0_}%~ $ '
```

## Arithmetic and Math Functions

```bash
# WHY: Advanced arithmetic
result=$((2.5 * 3.7))          # Floating point (requires zsh/mathfunc)

# WHY: Math functions (load module first)
zmodload zsh/mathfunc
echo $(( sqrt(16) ))           # 4.0
echo $(( sin(3.14159 / 2) ))   # 1.0
echo $(( log(10) ))            # 2.302585...
echo $(( exp(1) ))             # 2.718281...
echo $(( abs(-5) ))            # 5
echo $(( ceil(3.2) ))          # 4
echo $(( floor(3.8) ))         # 3
echo $(( rand(100) ))          # Random number 0-99

# WHY: Bitwise operations
echo $(( 5 & 3 ))              # 1 (AND)
echo $(( 5 | 3 ))              # 7 (OR)
echo $(( 5 ^ 3 ))              # 6 (XOR)
echo $(( ~5 ))                 # -6 (NOT)
echo $(( 8 >> 2 ))             # 2 (right shift)
echo $(( 2 << 3 ))             # 16 (left shift)
```

## Conditional Expressions

```bash
# WHY: Extended test operators
# [[ -ef ]] - Same file (checks inodes)
if [[ file1 -ef file2 ]]; then
  echo "Same file"
fi

# WHY: [[ -nt ]] - Newer than
if [[ file1 -nt file2 ]]; then
  echo "file1 is newer"
fi

# WHY: [[ -ot ]] - Older than
if [[ file1 -ot file2 ]]; then
  echo "file1 is older"
fi

# WHY: String matching with patterns
if [[ "$string" == (foo|bar)* ]]; then
  echo "Starts with foo or bar"
fi

# WHY: Numeric comparisons in [[]]
if [[ $count -gt 10 ]]; then
  echo "Greater than 10"
fi

# WHY: Array membership test
array=(red green blue)
if (( ${array[(ie)green]} <= ${#array} )); then
  echo "green is in array"
fi
```

## Modules and Built-ins

```bash
# WHY: Load modules for extended functionality
zmodload zsh/datetime          # Date/time functions
echo $EPOCHSECONDS             # Unix timestamp

zmodload zsh/stat              # File stat functions
stat -H info file.txt
echo "$info[size]"

zmodload zsh/system            # System calls
sysopen -w -o cloexec -u 3 output.txt
echo "data" >&3
sysseek -u 3 0                 # Seek to beginning

zmodload zsh/net/tcp           # TCP functions
ztcp remote.host.com 80
# Send HTTP request through $REPLY

zmodload zsh/regex             # PCRE regex
[[ "test@example.com" -regex-match '\w+@\w+\.\w+' ]]

# WHY: Built-in file operations
zmodload zsh/files
mkdir -p /path/to/dir          # Built-in mkdir
rm -f file.txt                 # Built-in rm
ln -s target link              # Built-in ln
```

## History Features

```bash
# WHY: History expansion
!!                             # Last command
!$                             # Last argument of last command
!^                             # First argument of last command
!*                             # All arguments of last command
!:2                            # Second argument of last command
!:2-4                          # Arguments 2-4 of last command

# WHY: Search history
!?pattern                      # Last command containing pattern
^old^new                       # Replace old with new in last command

# WHY: History modifiers
!!:s/old/new/                  # Substitute in last command
!!:gs/old/new/                 # Global substitute
!!:t                           # Basename only
!!:h                           # Dirname only
!!:r                           # Remove extension
!!:e                           # Extension only

# WHY: History options
setopt HIST_IGNORE_DUPS        # Don't record duplicates
setopt HIST_IGNORE_SPACE       # Ignore commands starting with space
setopt SHARE_HISTORY           # Share history across sessions
setopt INC_APPEND_HISTORY      # Append immediately, not on shell exit
```

## Completion System

```bash
# WHY: Initialize completion system
autoload -Uz compinit
compinit

# WHY: Enable menu completion
zstyle ':completion:*' menu select

# WHY: Case-insensitive completion
zstyle ':completion:*' matcher-list 'm:{a-zA-Z}={A-Za-z}'

# WHY: Completion colors
zstyle ':completion:*' list-colors ${(s.:.)LS_COLORS}

# WHY: Group completions
zstyle ':completion:*' group-name ''
zstyle ':completion:*:descriptions' format '%B%d%b'

# WHY: Completion caching
zstyle ':completion:*' use-cache on
zstyle ':completion:*' cache-path ~/.zsh/cache

# WHY: Verbose completion
zstyle ':completion:*' verbose yes

# WHY: Custom completion function
_my_command() {
  local -a options
  options=(
    'start:Start the service'
    'stop:Stop the service'
    'restart:Restart the service'
  )
  _describe 'command' options
}
compdef _my_command my_command
```

## Zsh-Specific Options

```bash
# WHY: Enable/disable options
setopt AUTO_CD                 # cd by typing directory name
setopt AUTO_PUSHD              # Make cd push to directory stack
setopt PUSHD_IGNORE_DUPS       # Don't push duplicates
setopt CORRECT                 # Spell correction for commands
setopt CORRECT_ALL             # Spell correction for all arguments
setopt EXTENDED_GLOB           # Extended globbing patterns
setopt NO_CASE_GLOB            # Case-insensitive globbing
setopt NUMERIC_GLOB_SORT       # Sort numerically when possible
setopt RC_EXPAND_PARAM         # Array expansion with params

# WHY: Check if option is set
if [[ -o AUTO_CD ]]; then
  echo "AUTO_CD is enabled"
fi
```

## Key Bindings and ZLE

```bash
# WHY: Load ZLE (Zsh Line Editor)
autoload -Uz edit-command-line
zle -N edit-command-line

# WHY: Bind keys
bindkey '^Xe' edit-command-line           # Ctrl-X,e to edit in $EDITOR
bindkey '^[[A' history-search-backward    # Up arrow searches history
bindkey '^[[B' history-search-forward     # Down arrow searches history

# WHY: Custom widget
my-widget() {
  BUFFER="echo 'Custom widget triggered'"
  zle accept-line
}
zle -N my-widget
bindkey '^X^M' my-widget                  # Ctrl-X,Ctrl-M
```

## Key Reminders

- Zsh arrays are 1-indexed by default (unlike Bash's 0-indexed)
- Use glob qualifiers for powerful file filtering
- Parameter expansion flags provide extensive string manipulation
- Load modules with `zmodload` for additional functionality
- Zsh doesn't split words by default (unlike Bash)
- Use `emulate` command to switch between shell emulation modes
- Zsh has excellent completion system - leverage it
- Check Zsh version for feature availability
- Document Zsh-specific features clearly in scripts
- Consider portability if script might run on other shells
