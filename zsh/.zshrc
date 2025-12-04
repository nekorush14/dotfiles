# Set History conf
HISTFILE=~/.zsh_history
HISTSIZE=10000
SAVEHIST=10000
setopt share_history
setopt hist_ignore_all_dups
setopt hist_ignore_space

# General conf
autoload -Uz colors ; colors
export EDITOR=nvim
bindkey -e
bindkey '^[[Z' reverse-menu-complete
setopt no_flow_control
setopt extended_glob
setopt auto_pushd
setopt pushd_ignore_dups
setopt auto_param_keys
setopt correct
# setopt correct_all
zstyle ':completion:*:sudo:*' command-path /usr/local/sbin /usr/local/bin \
                   /usr/sbin /usr/bin /sbin /bin /usr/X11R6/bin
zstyle ':completion:*:processes' command 'ps x -o pid,s,args'
setopt noautoremoveslash
umask 022
ulimit -c 0

# Completion
autoload -Uz compinit ; compinit
setopt complete_in_word
setopt correct
zstyle ':completion:*' menu select
setopt list_packed
export LSCOLORS=Exfxcxdxbxegedabagacad
export LS_COLORS='di=01;34:ln=01;35:so=01;32:ex=01;31:bd=46;34:cd=43;34:su=41;30:sg=46;30:tw=42;30:ow=43;30'
zstyle ':completion::complete:*' use-cache true
autoload -U colors ; colors ; zstyle ':completion:*' list-colors "${LS_COLORS}"
zstyle ':completion:*' matcher-list 'm:{a-z}={A-Z}'
zstyle ':completion:*:manuals' separate-sections true
setopt magic_equal_subst

# Set PATH
fpath=(.zsh/zsh-completions/src $fpath)

export GOPATH=$HOME/Repositories/Go
export PATH="$GOPATH/bin:$PATH"

path=(
  /opt/homebrew/bin(N-/)
  /opt/homebrew/sbin(N-/)
  /usr/bin
  /usr/sbin
  /bin
  /sbin
  /usr/local/bin(N-/)
  /usr/local/sbin(N-/)
  /Library/Apple/usr/bin
  /Applications/JetBrains Toolbox.app/Contents/scripts
  $HOME/.local/bin
  $HOME/.cargo/bin
  $HOME/Library/Android/sdk/platform-tools
  /opt/homebrew/bin
  $(brew --prefix)/bin
  /Applications/RubyMine.app/Contents/MacOS
  $path
)

if type brew &>/dev/null; then
  FPATH=$(brew --prefix)/share/zsh-completions:$FPATH
  source $(brew --prefix)/share/zsh-autosuggestions/zsh-autosuggestions.zsh
  autoload -Uz compinit && compinit
fi

# Environment variables
export SNDCPY_HOME="$HOME/Library/sndcpy-v1.1"
export SNDCPY_APK="$HOME/Library/sndcpy-v1.1/sndcpy.apk"
export VLC="/Applications/VLC.app/Contents/MacOS/VLC"
export GPG_TTY=$(tty)

# starship
eval "$(starship init zsh)"

# # Initialize zoxide
eval "$(zoxide init --cmd cd zsh)"

# JAVA_HOME
# export JAVA_HOME=$HOME/Library/Java/JavaVirtualMachines/temurin-17.0.7/Contents/Home

# pyenv
export VIRTUAL_ENV_DISABLE_PROMPT=1
# export PYENV_ROOT="$HOME/.pyenv"
# export PATH="$PYENV_ROOT/bin:$PATH"
# eval "$(pyenv init --path)"
# eval "$(pyenv init -)"
export PYENV_ROOT="$HOME/.pyenv"
command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"

# Set alias
alias g='$(brew --prefix)/bin/git'
alias ls='eza --icons --git'
alias ll='eza --icons --git --time-style relative -l'
alias la='eza --icons --git --time-style relative -la'
alias lla=la
alias ltl='eza --icons --git -TL=3 -I "node_module|.git|miniconda3|Library|Applications"'
alias lta='eza --icons --git -TL=3 -la -I "node_module|.git|miniconda3|Library|Applications"'
alias cat='bat'
alias du='dust'
alias df='duf'
alias grep='rg'
alias top='btm'
alias lg='lazygit'
alias ld='lazydocker'
alias scrcpy="scrcpy --audio-codec=aac"
alias vlc='/Applications/VLC.app/Contents/MacOS/VLC'
alias bvim='/bin/vim'
alias v='nvim'
alias vim='nvim'
alias ocat='/bin/cat'
alias tree='eza --tree --icons --git-ignore'
alias treeall='eza --tree --all --icons --git-ignore'
alias fd='fdfind'
alias awslocal="AWS_ACCESS_KEY_ID=test AWS_SECRET_ACCESS_KEY=test AWS_DEFAULT_REGION=${DEFAULT_REGION:-$AWS_DEFAULT_REGION} aws --endpoint-url=http://${LOCALSTACK_HOST:-localhost}:4566"
alias spt='spotify_player'
alias csr='cursor'
alias cursira='cursor-agent'
alias csra='cursor-agent'
alias ghqg='ghq get -p'
alias ghqgs='ghq get -p --shallow'
alias ghqu='ghq get -p -u'
alias rm="SAFE_RM_CONFIG=${HOME}/.config/safe-rm/safe-rm.conf safe-rm"
alias tdw="tmux-default-window.sh"
alias wm-reset="yabai --restart-service && skhd --restart-service"
alias imgcat="viu"

[ -f ~/.fzf.zsh ] && source ~/.fzf.zsh

export FZF_DEFAULT_COMMAND='rg --files --hidden --follow --glob "!**/.git/*"'
export FZF_DEFAULT_OPTS="
    --height 40% --reverse --border=sharp --margin=0,1
    --prompt='>> '
    --color=fg:#c0caf5,bg:#1a1b26,hl:#bb9af7
	  --color=fg+:#c0caf5,bg+:#1a1b26,hl+:#7dcfff
	  --color=info:#7aa2f7,prompt:#7dcfff,pointer:#7dcfff 
	  --color=marker:#9ece6a,spinner:#9ece6a,header:#9ece6a
"

# for finding files in current directories
export FZF_CTRL_T_COMMAND="$FZF_DEFAULT_COMMAND"
export FZF_CTRL_T_OPTS="
    --preview 'bat --color=always --style=header,grid {}'
    --preview-window=right:60%
"

# Ref: https://www.josean.com/posts/7-amazing-cli-tools
export FZF_ALT_R_OPTS="--preview 'eza --tree --icons --color=always {} | head -200'"

# Ref: https://wonderwall.hatenablog.com/entry/2017/10/06/063000
export FZF_CTRL_R_OPTS="
    --preview 'echo {}' --preview-window down:3:hidden:wrap --bind '?:toggle-preview'
"

# Ref: https://www.josean.com/posts/7-amazing-cli-tools
# Advanced customization of fzf options via _fzf_comprun function
# - The first argument to the function is the name of the command.
# - You should make sure to pass the rest of the arguments to fzf.
_fzf_comprun() {
  local command=$1
  shift

  case "$command" in
    cd)           fzf --preview 'eza --tree --icons --color=always {} | head -200' "$@" ;;
    export|unset) fzf --preview "eval 'echo $'{}"         "$@" ;;
    ssh)          fzf --preview 'dig {}'                   "$@" ;;
    *)            fzf --preview "bat -n --color=always --line-range :500 {}" "$@" ;;
  esac
}

# ghq
function ghq-fzf() {
  local src=$(ghq list | fzf --preview "bat --color=always --style=header,grid --line-range :80 $(ghq root)/{}/README.*")
  if [ -n "$src" ]; then
    BUFFER="cd $(ghq root)/$src"
    zle accept-line
  fi
  zle -R -c
}
zle -N ghq-fzf
bindkey '^g' ghq-fzf

# Initialize fzf
source <(fzf --zsh)

# lazygit
export XDG_CONFIG_HOME=${HOME}/.config

# # asdf setup
# export PATH="${ASDF_DATA_DIR:-$HOME/.asdf}/shims:$PATH"
# # append completions to fpath
# fpath=(${ASDF_DATA_DIR:-$HOME/.asdf}/completions $fpath)
# initialise completions with ZSH's compinit
autoload -Uz compinit && compinit

# Yazi config
function y() {
	local tmp="$(mktemp -t "yazi-cwd.XXXXXX")" cwd
	yazi "$@" --cwd-file="$tmp"
	if cwd="$(command cat -- "$tmp")" && [ -n "$cwd" ] && [ "$cwd" != "$PWD" ]; then
		builtin cd -- "$cwd"
	fi
	rm -f -- "$tmp"
}

# gh-copilot config
if command -v gh &>/dev/null; then
  if command -v gh-copilot &>/dev/null; then
    eval "$(gh-copilot init --zsh)"
  fi
fi

# Ruby config
[[ -d ~/.rbenv  ]] && \
  export PATH=${HOME}/.rbenv/bin:${PATH} && \
  eval "$(rbenv init -)"

# Node.js config
eval "$(nodenv init -)"

# tmux conf
function ide() {
  tmux split-window -v -p 25
  tmux split-window -h -p 50
}

# Local only source file
[ -f ~/.zshrc.local ] && source ~/.zshrc.local || true



# Load Angular CLI autocompletion.
source <(ng completion script)

# Added by LM Studio CLI (lms)
export PATH="$PATH:$HOME/.lmstudio/bin"
# End of LM Studio CLI section

