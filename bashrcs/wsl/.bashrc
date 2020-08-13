#####                                                                      #####
#    _               _                 __             __        ______  _      #
#   | |__   __ _ ___| |__  _ __ ___   / _| ___  _ __  \ \      / / ___|| |     #
#   | '_ \ / _` / __| '_ \| '__/ __| | |_ / _ \| '__|  \ \ /\ / /\___ \| |     #
#  _| |_) | (_| \__ \ | | | | | (__  |  _| (_) | |      \ V  V /  ___) | |___  #
# (_)_.__/ \__,_|___/_| |_|_|  \___| |_|  \___/|_|       \_/\_/  |____/|_____| #
#                                                                              #
#####                                                                      #####

# for setting history length see HISTSIZE and HISTFILESIZE in bash(1)
HISTSIZE=1000
HISTFILESIZE=2000

# for PS1 settings
if [ "$color_prompt" = yes ]; then
    PS1='${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u\[\033[00m\]:[\[\033[01;33m\]\w\[\033[00m\]]\n\[\033[00m\]\$:'
else
    PS1='${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u\[\033[00m\]:[\[\033[01;33m\]\w\[\033[00m\]]\n\[\033[00m\]\$:'
fi

unset color_prompt force_color_prompt

# Set JAVA_HOME
export JAVA_HOME=/usr/lib/jvm/java-8-oracle
export PATH=$PATH:$JAVA_HOME/bin

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

# Class path for jdbc
# export CLASSPATH=$CLASSPATH:/usr/share/java/mysql.jar

# Set nodebrew path
export PATH=$HOME/.nodebrew/current/bin:$PATH

# Set library path for macab
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/lib/

# Set local bainary path
export PATH=$HOME/bin:$PATH

# Set defaul text editor
export EDITOR=vim

# set user functions
function open() {
  xdg-open "$@" &
}

# Clipboard alias
alias pbcopy='xsel --clipboard --input'
alias py=python
alias ct=cat
alias vim=nvim
