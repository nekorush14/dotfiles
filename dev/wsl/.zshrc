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
source ~/.zsh/zsh-autosuggestions/zsh-autosuggestions.zsh

typeset -U path PATH
path=(
  $HOME/.local/bin
  $HOME/miniconda3/bin
  $path
)

# Set PATH, MANPATH, etc., for Homebrew.
eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"

# Set Prompt using oh-my-posh
eval "$(oh-my-posh init zsh --config ~/.posh-theme.omp.json --manual)"

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

# Conda config
# conda config --set auto_activate_base false

# Windows Intergration
function open() { /mnt/c/Windows/system32/cmd.exe /c start $(wslpath -w $1) }
alias pbcopy="/mnt/c/Windows/System32/clip.exe"
alias explorer="/mnt/c/Windows/explorer.exe"


# >>> conda initialize >>>
# !! Contents within this block are managed by 'conda init' !!
__conda_setup="$('/home/l10es/miniconda3/bin/conda' 'shell.zsh' 'hook' 2> /dev/null)"
if [ $? -eq 0 ]; then
    eval "$__conda_setup"
else
    if [ -f "/home/l10es/miniconda3/etc/profile.d/conda.sh" ]; then
        . "/home/l10es/miniconda3/etc/profile.d/conda.sh"
    else
        export PATH="/home/l10es/miniconda3/bin:$PATH"
    fi
fi
unset __conda_setup
# <<< conda initialize <<<

