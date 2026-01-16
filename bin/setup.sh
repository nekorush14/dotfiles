#!/usr/bin/env bash
# Setup script for dotfiles
# Creates symlinks from configs/ to their respective target locations
set -euo pipefail

# Default dotfiles directory (can be overridden by DOTFILES_DIR env var)
DOTFILES_DIR="${DOTFILES_DIR:-$HOME/Developer/ghq/github.com/nekorush14/dotfiles}"
CONFIGS_DIR="$DOTFILES_DIR/configs"
DRY_RUN=false

# Color output helpers
info() { printf '\033[0;34m[INFO]\033[0m %s\n' "$1"; }
success() { printf '\033[0;32m[OK]\033[0m %s\n' "$1"; }
skip() { printf '\033[0;33m[SKIP]\033[0m %s\n' "$1"; }
error() { printf '\033[0;31m[ERROR]\033[0m %s\n' "$1" >&2; }

# Show usage
usage() {
  cat <<EOF
Usage: $(basename "$0") [OPTIONS]

Setup dotfiles by creating symlinks from configs/ to target locations.

Options:
  -n, --dry-run    Show what would be done without making changes
  -h, --help       Show this help message

Environment variables:
  DOTFILES_DIR     Path to dotfiles repository (default: ~/Developer/ghq/github.com/nekorush14/dotfiles)
EOF
}

# Parse arguments
parse_args() {
  while [[ $# -gt 0 ]]; do
    case "$1" in
      -n|--dry-run)
        DRY_RUN=true
        shift
        ;;
      -h|--help)
        usage
        exit 0
        ;;
      *)
        error "Unknown option: $1"
        usage
        exit 1
        ;;
    esac
  done
}

# Create symlink with backup
# Args: $1=source, $2=destination
create_symlink() {
  local src="$1"
  local dst="$2"

  # Check if source exists
  if [[ ! -e "$src" ]]; then
    error "Source does not exist: $src"
    return 1
  fi

  # Skip if correct symlink already exists
  if [[ -L "$dst" ]] && [[ "$(readlink "$dst")" == "$src" ]]; then
    skip "$dst (already linked)"
    return 0
  fi

  # Backup existing file/directory/symlink
  if [[ -e "$dst" ]] || [[ -L "$dst" ]]; then
    if [[ "$DRY_RUN" == true ]]; then
      info "[DRY-RUN] Would backup: $dst -> ${dst}.bak"
    else
      mv "$dst" "${dst}.bak"
      info "Backed up: $dst -> ${dst}.bak"
    fi
  fi

  # Create parent directory if needed
  local parent_dir
  parent_dir="$(dirname "$dst")"
  if [[ ! -d "$parent_dir" ]]; then
    if [[ "$DRY_RUN" == true ]]; then
      info "[DRY-RUN] Would create directory: $parent_dir"
    else
      mkdir -p "$parent_dir"
      info "Created directory: $parent_dir"
    fi
  fi

  # Create symlink
  if [[ "$DRY_RUN" == true ]]; then
    info "[DRY-RUN] Would link: $src -> $dst"
  else
    ln -s "$src" "$dst"
    success "$dst -> $src"
  fi
}

# Main setup function
main() {
  parse_args "$@"

  # Verify configs directory exists
  if [[ ! -d "$CONFIGS_DIR" ]]; then
    error "Configs directory not found: $CONFIGS_DIR"
    error "Please set DOTFILES_DIR environment variable correctly"
    exit 1
  fi

  if [[ "$DRY_RUN" == true ]]; then
    info "=== DRY-RUN MODE ==="
    info "No changes will be made"
    echo
  fi

  info "Setting up dotfiles from: $CONFIGS_DIR"
  echo

  # Define symlink mappings: source -> destination
  # Format: "source_relative_path:destination_absolute_path"
  local mappings=(
    # ~/.config/ targets
    "bat:$HOME/.config/bat"
    "ghostty:$HOME/.config/ghostty"
    "karabiner:$HOME/.config/karabiner"
    "lazygit:$HOME/.config/lazygit"
    "mpd:$HOME/.config/mpd"
    "nvim:$HOME/.config/nvim"
    "rmpc:$HOME/.config/rmpc"
    "safe-rm:$HOME/.config/safe-rm"
    "skhd:$HOME/.config/skhd"
    "spotify-player:$HOME/.config/spotify-player"
    "superfile:$HOME/.config/superfile"
    "yabai:$HOME/.config/yabai"
    "yazi:$HOME/.config/yazi"
    "zellij:$HOME/.config/zellij"
    "starship.toml:$HOME/.config/starship.toml"

    # VS Code (special path)
    "code:$HOME/.config/Code/User"

    # Home directory targets
    "claude:$HOME/.claude"
    "codex:$HOME/.codex"
    "cursor:$HOME/.cursor"
    "gemini:$HOME/.gemini"
    "serena:$HOME/.serena"

    # Single file symlinks
    "tmux/.tmux.conf:$HOME/.tmux.conf"
    "zsh/.zshrc:$HOME/.zshrc"
  )

  # Process each mapping
  for mapping in "${mappings[@]}"; do
    local src_rel="${mapping%%:*}"
    local dst="${mapping#*:}"
    local src="$CONFIGS_DIR/$src_rel"

    create_symlink "$src" "$dst"
  done

  echo
  if [[ "$DRY_RUN" == true ]]; then
    info "=== DRY-RUN COMPLETE ==="
    info "Run without -n to apply changes"
  else
    success "=== Setup complete ==="
  fi
}

main "$@"
