#!/bin/bash

# Constants
readonly NOTIFIER="/opt/homebrew/bin/terminal-notifier"

# Set notification parameters based on type (input validation via case)
case "$1" in
permission)
  title="🚧 Claude Code"
  subtitle="Permission Required"
  message="Claude Code is requesting permission."
  sound="Glass"
  ;;
# plan)
#   title="📋 Claude Code"
#   subtitle="Plan Ready"
#   message="プランの確認をお願いします"
#   sound="Ping"
#   ;;
stop)
  title="✅ Claude Code"
  subtitle="Completed"
  message="Task has been completed."
  sound="Hero"
  ;;
*)
  # Invalid input - exit silently
  exit 0
  ;;
esac

# Send notification with terminal-notifier (all variables quoted)
"$NOTIFIER" \
  -title "$title" \
  -subtitle "$subtitle" \
  -message "$message" \
  -sound "$sound" \
  -group "claude-code"
