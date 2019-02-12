source /usr/local/etc/bash_completion.d/git-prompt.sh
source /usr/local/etc/bash_completion.d/git-completion.bash

GIT_PS1_SHOWDIRTYSTATE=true
# for PS1 settings
if [ "$color_prompt" = yes ]; then
    PS1='${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u\[\033[00m\]:[\[\033[01;33m\]\w\[\033[00m\]]\n\[\033[31m\]$(__git_ps1)\[\033[00m\]\$:'
else
    PS1='${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u\[\033[00m\]:[\[\033[01;33m\]\w\[\033[00m\]]\n\[\033[31m\]$(__git_ps1)\[\033[00m\]\$:'
fi

export CLICOLOR=1
export LSCOLORS=gxfxcxdxbxegedabagacad
export LC_CTYPE="en_US.UTF-8"
export LESS='-R'
export LESSOPEN='| /opt/local/bin/src-hilite-lesspipe.sh %s'

export PATH=/usr/local/Cellar/git/2.19.0_2/bin:$PATH
export PATH=$HOME/.nodebrew/current/bin:$PATH
export PATH=/Users/mitsuhiro/anaconda3/bin:$PATH
export PATH=$HOME/Repositories/dotfiles/tmux/bin:$PATH
export PATH=$HOME/Library/Flutter/bin:$PATH

shopt -u histappend
share_history(){
    history -a
    history -c
    history -r
}
PROMPT_COMMAND='share_history'

# Alias
alias py='python'
alias ct='cat'
alias jn='jupyter notebook --port 8888'
alias jl='jupyter lab --port 8889'

