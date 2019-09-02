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
if [ "$color_prompt" = yes ]; then
    PS1='${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u@\h\[\033[00m\]:[\[\033[01;33m\]\w\[\033[00m\]]\n\[\033[31m\]$(__git_ps1)\[\033[00m\]\$:'
else
    PS1='${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u@\h\[\033[00m\]:[\[\033[01;33m\]\w\[\033[00m\]]\n\[\033[31m\]$(__git_ps1)\[\033[00m\]\$:'
fi

unset color_prompt force_color_prompt

# Set JAVA_HOME
export JAVA_HOME=/usr/lib/jvm/java-9-openjdk-amd64
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

# Set local bainary path
export PATH=$HOME/bin:$PATH
export PATH=$HOME/Repositories/dotfiles/tmux/bin:$PATH
export PATH=$HOME/Repositories/dotfiles/bin:$PATH
export PATH=/usr/local/cuda/bin:$PATH

# Set defaul text editor
export EDITOR=vim


# git-completion.bash / git-prompt.sh
# if [ -f $HOME/Utils/git-completion.bash ]; then
#     source $HOME/Utils/git-completion.bash
# fi
# if [ -f $HOME/Utils/git-prompt.sh ]; then
#     source $HOME/Utils/git-prompt.sh
# fi
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
alias py='python'
alias ct='cat'
alias ls='ls --color=auto'
alias jn='jupyter notebook --port 8888'
alias jl='jupyter lab --port 8889'

