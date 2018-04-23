# for setting history length see HISTSIZE and HISTFILESIZE in bash(1)
HISTSIZE=1000
HISTFILESIZE=2000

# for PS1 settings
if [ "$color_prompt" = yes ]; then
    PS1='${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u\[\033[00m\]:[\[\033[01;33m\]\w\[\033[00m\]]\n\[\033[00m\]\$:'
else
    PS1='${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u\[\033[00m\]:[\[\033[01;33m\]\w\[\033[00m\]]\n\[\033[00m\]\$:'
fi

# PS1 settings for macOS
# if [ "$color_prompt" = yes ]; then
#     PS1='${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u\[\033[00m\]:[\[\033[01;33m\]\w\[\033[00m\]]\n\[\033[31m\]$(__git_ps1)\[\033[00m\]\$:'
# else
#     PS1='${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u\[\033[00m\]:[\[\033[01;33m\]\w\[\033[00m\]]\n\[\033[31m\]$(__git_ps1)\[\033[00m\]\$:'
# fi
unset color_prompt force_color_prompt

# Set JAVA_HOME
export JAVA_HOME=/usr/lib/jvm/java-8-oracle
export PATH=$PATH:$JAVA_HOME/bin

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

# Alias for Linux system
# alias OPEN_G='open'
# alias pbcopy='xsel --clipboard --input'

# For macOS
source /usr/local/etc/bash_completion.d/git-prompt.sh
source /usr/local/etc/bash_completion.d/git-completion.bash
GIT_PS1_SHOWDIRTYSTATE=true
export CLICOLOR=1
export LSCOLORS=gxfxcxdxbxegedabagacad

