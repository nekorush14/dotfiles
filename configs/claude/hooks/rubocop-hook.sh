#!/bin/bash

# Exit immediately if any command fails
set -e

# Change to project directory if CLAUDE_PROJECT_DIR is set
if [ -n "$CLAUDE_PROJECT_DIR" ]; then
    cd "$CLAUDE_PROJECT_DIR"
fi

# Check if rubocop is available
if ! command -v rubocop &> /dev/null; then
    echo "Warning: rubocop not found in PATH" >&2
    exit 0
fi

# Check if we're in a Ruby/Rails project
is_ruby_project() {
    # Check for common Ruby project indicators
    [ -f "Gemfile" ] || \
    [ -f ".rubocop.yml" ] || \
    [ -f ".rubocop.yaml" ] || \
    [ -f "Rakefile" ] || \
    [ -f "config.ru" ] || \
    [ -f "Gemfile.lock" ] || \
    [ -d "app/models" ] || \
    [ -d "config/application.rb" ] || \
    [ -f "*.gemspec" ] || \
    find . -maxdepth 2 -name "*.rb" -type f 2>/dev/null | head -1 | grep -q "."
}

if ! is_ruby_project; then
    # Not a Ruby project, exit silently
    exit 0
fi

# First, try to auto-correct what we can
rubocop --autocorrect-all --format quiet > /dev/null 2>&1 || true

# Then check for remaining issues
RUBOCOP_OUTPUT=$(rubocop --format simple 2>&1)
RUBOCOP_EXIT_CODE=$?

if [ $RUBOCOP_EXIT_CODE -ne 0 ]; then
    # Format the output for Claude Code
    echo "Rubocopで以下のコードスタイル違反が検出されました。修正してください："
    echo ""
    echo "$RUBOCOP_OUTPUT"
    echo ""
    echo "自動修正できない問題があります。手動で修正が必要です。"

    # Exit with code 2 to prompt Claude Code for fixes
    exit 2
fi

# No issues found
exit 0