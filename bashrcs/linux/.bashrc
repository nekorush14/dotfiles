#######                                                                     #######
#    _               _                 __              _     _                    #
#   | |__   __ _ ___| |__  _ __ ___   / _| ___  _ __  | |   (_)_ __  _   ___  __  #
#   | '_ \ / _` / __| '_ \| '__/ __| | |_ / _ \| '__| | |   | | '_ \| | | \ \/ /  #
#  _| |_) | (_| \__ \ | | | | | (__  |  _| (_) | |    | |___| | | | | |_| |>  <   #
# (_)_.__/ \__,_|___/_| |_|_|  \___| |_|  \___/|_|    |_____|_|_| |_|\__,_/_/\_\  #
#                                                                                 #
######                                                                      #######

# for setting history length see HISTSIZE and HISTFILESIZE in bash(1)
HISTSIZE=1000
HISTFILESIZE=2000

# for PS1 settings
#if [ "$color_prompt" = yes ]; then
#    PS1='${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u@\h\[\033[00m\]:[\[\033[01;33m\]\w\[\033[00m\]]\n\[\033[31m\]$(__git_ps1)\[\033[00m\]\$:'
#else
#    PS1='${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u@\h\[\033[00m\]:[\[\033[01;33m\]\w\[\033[00m\]]\n\[\033[31m\]$(__git_ps1)\[\033[00m\]\$:'
#fi

function _update_ps1() {
    PS1="$($GOPATH/bin/powerline-go -error $? -modules venv,user,ssh,docker,docker-context,cwd,perms,git,hg,jobs,exit,newline,root -cwd-mode semifancy -jobs $(jobs -p | wc -l))"

    # Uncomment the following line to automatically clear errors after showing
    # them once. This not only clears the error for powerline-go, but also for
    # everything else you run in that shell. Don't enable this if you're not
    # sure this is what you want.

    #set "?"
}

if [ "$TERM" != "linux" ] && [ -f "$GOPATH/bin/powerline-go" ]; then
    PROMPT_COMMAND="_update_ps1; $PROMPT_COMMAND"
fi

unset color_prompt force_color_prompt

export GOPATH=$HOME/go
export PATH=$PATH:/usr/local/go/bin
export GOROOT=/usr/lib/go


# Set JAVA_HOME
export JAVA_HOME=/usr/lib/jvm/jdk8u275-b01
export PATH=$PATH:$JAVA_HOME/bin

# Class path for jdbc
# export CLASSPATH=$CLASSPATH:/usr/share/java/mysql.jar

# Set nodebrew path
export PATH=$HOME/.nodebrew/current/bin:$PATH

# Set library path for macab
# export LD_LIBRARY_PATH=/usr/local/lib/:$LD_LIBRARY_PATH

# LD_LIBRARY_PATH for cuda
export LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH
# export LD_LIBRARY_PATH=/usr/local/cuda/extras/CUPTI/lib64:$LD_LIBRARY_PATH

# Set local library path
export PATH=$HOME/bin:$PATH
export PATH=$HOME/Repositories/dotfiles/tmux/bin:$PATH
export PATH=$HOME/Repositories/dotfiles/bin:$PATH
export PATH=$HOME/lib/flutter:$PATH
export PATH=$HOME/lib/flutter/bin:$PATH
export PATH=/usr/local/cuda/bin:$PATH
export PATH=$HOME/miniconda3/bin:$PATH

export TMPDIR="/tmp"

# Set defaul text editor
export EDITOR=vim

# UID and GID
export U_ID=$(id -u)
export G_ID=$(id -g)

# git-completion.bash / git-prompt.sh
if [ -f $HOME/Utils/git-completion.bash ]; then
    source $HOME/Utils/git-completion.bash
fi
if [ -f $HOME/Utils/git-prompt.sh ]; then
    source $HOME/Utils/git-prompt.sh
fi
GIT_PS1_SHOWDIRTYSTATE=true
GIT_PS1_SHOWUNTRACKEDFILES=true
GIT_PS1_SHOWSTASHSTATE=true
GIT_PS1_SHOWUPSTREAM=auto

# set user functions
function open() {
  xdg-open "$@" &
}

# Alias for Linux system
alias pbcopy='xsel --clipboard --input'
alias ls='ls --color=auto'
# alias vim='nvim'

[ -f ~/.fzf.bash ] && source ~/.fzf.bash

export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion

# >>> conda initialize >>>
# !! Contents within this block are managed by 'conda init' !!
__conda_setup="$('/home/mitsuhiro/miniconda3/bin/conda' 'shell.bash' 'hook' 2> /dev/null)"
if [ $? -eq 0 ]; then
    eval "$__conda_setup"
else
    if [ -f "/home/mitsuhiro/miniconda3/etc/profile.d/conda.sh" ]; then
        . "/home/mitsuhiro/miniconda3/etc/profile.d/conda.sh"
    else
        export PATH="/home/mitsuhiro/miniconda3/bin:$PATH"
    fi
fi
unset __conda_setup
# <<< conda initialize <<<

function gi() { curl -sL https://www.toptal.com/developers/gitignore/api/$@ ;}
