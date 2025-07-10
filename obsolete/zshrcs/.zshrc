# Fig pre block. Keep at the top of this file.
# [[ -f "$HOME/.fig/shell/zshrc.pre.zsh" ]] && builtin source "$HOME/.fig/shell/zshrc.pre.zsh"
typeset -U path PATH

# PATH

export GOPATH=$HOME/Repositories/Go
export PATH="$GOPATH/bin:$PATH"

path=(
  /home/linuxbrew/.linuxbrew/bin
  /usr/bin
  /usr/sbin
  /bin
  /sbin
  /usr/local/bin(N-/)
  /usr/local/sbin(N-/)
  $HOME/.local/bin
  /usr/lib/wsl/lib
  '/mnt/c/Users/leica/AppData/Local/Programs/Microsoft VS Code/bin'
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

# CUDA
export PATH=/usr/local/cuda-12.6/bin${PATH:+:${PATH}}
export LD_LIBRARY_PATH=/usr/local/cuda-12.6/lib64:${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}

# OMP
# eval "$(oh-my-posh init zsh --config ~/.posh-theme.omp.json)"

# starship
eval "$(starship init zsh)"

# Set alias
alias vim='nvim'
alias git='$(brew --prefix)/bin/git'
alias ls='eza --icons --git'
alias ll='eza --icons --git --time-style relative -l'
alias la='eza --icons --git --time-style relative -la'
alias ltl='eza --icons --git -TL=3 -I "node_module|.git|miniconda3|Library|Applications"'
alias lta='eza --icons --git -TL=3 -la -I "node_module|.git|miniconda3|Library|Applications"'
alias cat='bat'
alias du='dust'
alias df='duf'
alias top='btm'
alias lg='lazygit'
alias ld='lazydocker'
# alias scrcpy="scrcpy --audio-codec=aac"
# alias vlc='/Applications/VLC.app/Contents/MacOS/VLC'

export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion

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
# __conda_setup="$('$HOME/miniconda3/bin/conda' 'shell.zsh' 'hook' 2> /dev/null)"
# if [ $? -eq 0 ]; then
#     eval "$__conda_setup"
# else
#     if [ -f "$HOME/miniconda3/etc/profile.d/conda.sh" ]; then
#         . "$HOME/miniconda3/etc/profile.d/conda.sh"
#     else
#         export PATH="$HOME/miniconda3/bin:$PATH"
#     fi
# fi
# unset __conda_setup
# <<< conda initialize <<<

# AWS config
complete -C '/usr/local/bin/aws_completer' aws

# Rust config
# source "$HOME/.cargo/env"

# Fig post block. Keep at the bottom of this file.
# [[ -f "$HOME/.fig/shell/zshrc.post.zsh" ]] && builtin source "$HOME/.fig/shell/zshrc.post.zsh"

# Load Angular CLI autocompletion.
# source <(ng completion script)

