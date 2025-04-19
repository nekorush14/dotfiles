# Set History conf
HISTFILE=~/.zsh_history
HISTSIZE=10000
SAVEHIST=10000
setopt share_history
setopt hist_ignore_all_dups
setopt hist_ignore_space

# General conf
autoload -Uz colors ; colors
export EDITOR=vim
bindkey -e
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
  $HOME/.local/bin
  $HOME/Library/Android/sdk/platform-tools
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
# eval "$(zoxide init zsh)"

# JAVA_HOME
# export JAVA_HOME=$HOME/Library/Java/JavaVirtualMachines/temurin-17.0.7/Contents/Home

# pyenv
export VIRTUAL_ENV_DISABLE_PROMPT=1
# export PYENV_ROOT="$HOME/.pyenv"
# export PATH="$PYENV_ROOT/bin:$PATH"
# eval "$(pyenv init --path)"
# eval "$(pyenv init -)"

# Set alias
# alias vim='lvim'
# alias nvim='lvim'
alias git='$(brew --prefix)/bin/git'
alias ls='eza --icons --git'
alias ll='eza --icons --git --time-style relative -l'
alias la='eza --icons --git --time-style relative -la'
alias lla=la
alias ltl='eza --icons --git -TL=3 -I "node_module|.git|miniconda3|Library|Applications"'
alias lta='eza --icons --git -TL=3 -la -I "node_module|.git|miniconda3|Library|Applications"'
alias cat='bat'
alias du='dust'
alias df='duf'
alias top='btm'
alias lg='lazygit'
alias ld='lazydocker'
alias scrcpy="scrcpy --audio-codec=aac"
alias vlc='/Applications/VLC.app/Contents/MacOS/VLC'
alias bvim='/bin/vim'
alias vim='nvim'
alias ocat='/bin/cat'
alias fd='fdfind'
alias awslocal="AWS_ACCESS_KEY_ID=test AWS_SECRET_ACCESS_KEY=test AWS_DEFAULT_REGION=${DEFAULT_REGION:-$AWS_DEFAULT_REGION} aws --endpoint-url=http://${LOCALSTACK_HOST:-localhost}:4566"

# export NVM_DIR="$HOME/.nvm"
# [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
# [ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion

[ -f ~/.fzf.zsh ] && source ~/.fzf.zsh

export FZF_DEFAULT_COMMAND='rg --files --hidden --follow --glob "!**/.git/*"'
export FZF_DEFAULT_OPTS="
    --height 40% --reverse --border=sharp --margin=0,1
    --prompt='>> ' --color=light
"

# for finding files in current directories
export FZF_CTRL_T_COMMAND="$FZF_DEFAULT_COMMAND"
export FZF_CTRL_T_OPTS="
    --preview 'bat --color=always --style=header,grid {}'
    --preview-window=right:60%
"

# Ref: https://wonderwall.hatenablog.com/entry/2017/10/06/063000
export FZF_CTRL_R_OPTS="
    --preview 'echo {}' --preview-window down:3:hidden:wrap --bind '?:toggle-preview'
"

# >>> conda initialize >>>
# !! Contents within this block are managed by 'conda init' !!
__conda_setup="$('/Users/l12s/miniconda3/bin/conda' 'shell.zsh' 'hook' 2> /dev/null)"
if [ $? -eq 0 ]; then
    eval "$__conda_setup"
else
    if [ -f "/Users/l12s/miniconda3/etc/profile.d/conda.sh" ]; then
        . "/Users/l12s/miniconda3/etc/profile.d/conda.sh"
    else
        export PATH="/Users/l12s/miniconda3/bin:$PATH"
    fi
fi
unset __conda_setup
# <<< conda initialize <<<

source "$HOME/.cargo/env"

# asdf setup
export PATH="${ASDF_DATA_DIR:-$HOME/.asdf}/shims:$PATH"
# append completions to fpath
fpath=(${ASDF_DATA_DIR:-$HOME/.asdf}/completions $fpath)
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

# Brewfile
if [ -f $(brew --prefix)/etc/brew-wrap ];then
  source $(brew --prefix)/etc/brew-wrap
fi
