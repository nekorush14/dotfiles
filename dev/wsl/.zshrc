# Set History conf
HISTFILE=~/.zsh_history
HISTSIZE=10000
SAVEHIST=10000
setopt appendhistory

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
setopt correct_all
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
typeset -U path PATH

path=(
  /usr/bin
  /usr/sbin
  /bin
  /sbin
  /usr/local/bin(N-/)
  /usr/local/sbin(N-/)
  /home/l12s/.local/bin
  /home/l12s/binn
)

# Set Plugins
# if type brew &>/dev/null; then
#   FPATH=$(brew --prefix)/share/zsh-completions:$FPATH
#   source $(brew --prefix)/share/zsh-autosuggestions/zsh-autosuggestions.zsh
#   autoload -Uz compinit && compinit
# fi
fpath=(.zsh/zsh-completions/src $fpath)
source ~/.zsh/zsh-autosuggestions/zsh-autosuggestions.zsh

# Set PATH, MANPATH, etc., for Homebrew.
eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"

# Set Prompt using oh-my-posh
eval "$(oh-my-posh init zsh --config ~/.posh-theme.omp.json)"

# Set alias
alias bvim='/bin/vim'
alias vim='nvim'
alias ls='lsd'
alias ll='lsd -l'
alias cat='bat'
alias bcat='/bin/cat'
alias du='dust'
alias df='duf'
alias top='btm'
alias lg='lazygit'
alias ld='lazydocker'
alias fd='fdfind'

# Windows Intergration
function open() { /mnt/c/Windows/system32/cmd.exe /c start $(wslpath -w $1) }
alias pbcopy="/mnt/c/Windows/System32/clip.exe"
alias explorer="/mnt/c/Windows/explorer.exe"
alias code="'/mnt/c/Users/leica/AppData/Local/Programs/Microsoft VS Code/bin'"

