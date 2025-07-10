#######                                                                                       ########
#    _               _                  __             __        ___           _                     #
#   | |__   __ _ ___| |__  _ __ __ _   / _| ___  _ __  \ \      / (_)_ __   __| | _____      _____   #
#   | '_ \ / _` / __| '_ \| '__/ __|  | |_ / _ \| '__\  \ \ /\ / /| | '_ \ / _` |/ _ \ \ /\ / / __|  #
#  _| |_) | (_| \__ \ | | | | | (__   |  _| (_) | |      \ V  V / | | | | | (_| | (_) \ V  V /\__ \  #
# (_)_.__/ \__,_|___/_| |_|_|  \___|  |_|  \___/|_|       \_/\_/  |_|_| |_|\__,_|\___/ \_/\_/ |___/  #
#                                                                                                    #
######                                                                                        ########

# for setting history length see HISTSIZE and HISTFILESIZE in bash(1)
HISTSIZE=1000
HISTFILESIZE=2000

# for PS1 settings
if [ "$color_prompt" = yes ]; then
    PS1='${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u@\h\[\033[00m\]:[\[\033[01;33m\]\w\[\033[00m\]]\n\[\033[31m\]$(__git_ps1)\[\033[00m\]\$:'
else
    PS1='${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u@\h\[\033[00m\]:[\[\033[01;33m\]\w\[\033[00m\]]\n\[\033[31m\]$(__git_ps1)\[\033[00m\]\$:'
fi

# eval "$(oh-my-posh init bash --config ~/lib/themes/iterm2cp.omp.json)"

unset color_prompt force_color_prompt

# Set JAVA_HOME
# export JAVA_HOME=/usr/lib/jvm/jdk8u275-b01
export PATH=$PATH:$JAVA_HOME/bin

# Class path for jdbc
# export CLASSPATH=$CLASSPATH:/usr/share/java/mysql.jar

# Set nodebrew path
export PATH=$HOME/.nodebrew/current/bin:$PATH

# Set library path for macab
export LD_LIBRARY_PATH=/usr/local/lib/:$LD_LIBRARY_PATH

# LD_LIBRARY_PATH for cuda
export LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH
export LD_LIBRARY_PATH=/usr/local/cuda/extras/CUPTI/lib64:$LD_LIBRARY_PATH

# Set local library path
export PATH=$HOME/bin:$PATH
export PATH=$HOME/Repositories/dotfiles/tmux/bin:$PATH
export PATH=$HOME/Repositories/dotfiles/bin:$PATH
export PATH=$HOME/lib/flutter:$PATH
export PATH=$HOME/lib/flutter/bin:$PATH
export PATH=/usr/local/cuda/bin:$PATH
export PATH=$HOME/anaconda3/bin:$PATH

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
alias tree='tree -N'

[ -f ~/.fzf.bash ] && source ~/.fzf.bash

lnkpath() { powershell -Command "(new-object -comobject wscript.shell).createShortcut(\"$1\").TargetPath"; }

cd () {
    if [ "`echo $1 | grep '.lnk'`" ]; then
        builtin cd `lnkpath $1`
    else
        builtin cd $1
    fi
}
