typeset -U path PATH

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
  /Users/l12s/.local/bin
)

if type brew &>/dev/null; then
  FPATH=$(brew --prefix)/share/zsh-completions:$FPATH
  source $(brew --prefix)/share/zsh-autosuggestions/zsh-autosuggestions.zsh
  autoload -Uz compinit && compinit
fi

eval "$(oh-my-posh init zsh --config ~/.posh-theme.omp.json)"

# Set alias
alias vim='nvim'
alias git='$(brew --prefix)/bin/git'
alias ls='lsd'
alias ll='lsd -l'
alias cat='bat'
alias du='dust'
alias df='duf'
alias top='btm'
alias lg='lazygit'
alias ld='lazydocker'


export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion

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
