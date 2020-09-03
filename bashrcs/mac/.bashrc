#######                                                                            #######
#    _               _                 __                                    ___  ____   #
#   | |__   __ _ ___| |__  _ __ ___   / _| ___  _ __   _ __ ___   __ _  ___ / _ \/ ___|  #
#   | '_ \ / _` / __| '_ \| '__/ __| | |_ / _ \| '__| | '_ ` _ \ / _` |/ __| | | \___ \  #
#  _| |_) | (_| \__ \ | | | | | (__  |  _| (_) | |    | | | | | | (_| | (__| |_| |___) | #
# (_)_.__/ \__,_|___/_| |_|_|  \___| |_|  \___/|_|    |_| |_| |_|\__,_|\___|\___/|____/  #
#                                                                                        #
#####                                                                              #######

source /usr/local/etc/bash_completion.d/git-prompt.sh
source /usr/local/etc/bash_completion.d/git-completion.bash

GIT_PS1_SHOWDIRTYSTATE=true
# for PS1 settings
if [ "$color_prompt" = yes ]; then
    PS1='${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u\[\033[00m\]:[\[\033[01;33m\]\w\[\033[00m\]]\n\[\033[31m\]$(__git_ps1)\[\033[00m\]\$:'
else
    PS1='${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u\[\033[00m\]:[\[\033[01;33m\]\w\[\033[00m\]]\n\[\033[31m\]$(__git_ps1)\[\033[00m\]\$:'
fi

# environment variables
export CLICOLOR=1
export LSCOLORS=gxfxcxdxbxegedabagacad
export LC_CTYPE="en_US.UTF-8"
export LC_ALL="en_US.UTF-8"
export LESS='-R'
export LESSOPEN='| /opt/local/bin/src-hilite-lesspipe.sh %s'

# Environment variable for llvm
export LDFLAGS="-L/usr/local/opt/llvm/lib"
export CPPFLAGS="-I/usr/local/opt/llvm/include"

# environment variable for Golang
export GOPATH=$HOME/go
export GO111MODULE=on
export GOBIN=${GOPATH//://bin:}/bin

# Environment variable for PATH
export PATH=/usr/local/Cellar/git/2.19.0_2/bin:$PATH
export PATH=$HOME/.nodebrew/current/bin:$PATH
export PATH=$HOME/anaconda3/bin:$PATH
export PATH=$HOME/Repositories/dotfiles/tmux/bin:$PATH
export PATH=$HOME/Library/Flutter/bin:$PATH
export PATH=${GOPATH//://bin:}/bin:$PATH
export PATH=$HOME/.fzf/bin:$PATH
export FZF_DEFAULT_COMMAND='rg --files --hidden --glob "!.git"'
export FZF_DEFAULT_OPTS='--height 30% --border'
export PATH=$HOME/Library/Android/sdk/platform-tools:$PATH
export PATH=/usr/local/opt/llvm/bin:$PATH

# fzf settings
export FZF_DEFAULT_COMMAND='rg --files --hidden --glob "!.git"'
export FZF_DEFAULT_OPTS='--height 30% --border'
[ -f ~/.fzf.zsh ] && source ~/.fzf.zsh

shopt -u histappend
share_history(){
    history -a
    history -c
    history -r
}
PROMPT_COMMAND='share_history'

# Alias
alias jn='jupyter notebook --port 8888'
alias jl='jupyter lab --port 8889'
alias tmux='tmux -u2'
alias vim='nvim'

# Auto run tmux command when terminal is start at first time
count=`ps aux | grep tmux | grep -v grep | wc -l`
if test $count -eq 0; then
    echo `tmux`
elif test $count -eq 1; then
    echo `tmux a`
fi
