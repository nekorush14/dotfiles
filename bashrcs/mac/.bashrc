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

# GIT_PS1_SHOWDIRTYSTATE=true
# for PS1 settings
# if [ "$color_prompt" = yes ]; then
#     PS1='${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u\[\033[00m\]:[\[\033[01;33m\]\w\[\033[00m\]]\n\[\033[31m\]$(__git_ps1)\[\033[00m\]\$:'
# else
#     PS1='${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u\[\033[00m\]:[\[\033[01;33m\]\w\[\033[00m\]]\n\[\033[31m\]$(__git_ps1)\[\033[00m\]\$:'
# fi
# eval "$(oh-my-posh init bash --config /opt/homebrew/opt/oh-my-posh/themes/iterm2.omp.json)"

[[ "$TERM_PROGRAM" == "vscode" ]] && . "$(code --locate-shell-integration-path bash)"

# environment variables
export CLICOLOR=1
export LSCOLORS=gxfxcxdxbxegedabagacad
export LC_CTYPE="en_US.UTF-8"
export LC_ALL="en_US.UTF-8"
export LESS='-R'
export LESSOPEN='| /opt/local/bin/src-hilite-lesspipe.sh %s'
export CHROME_EXECUTABLE="/Applications/Google Chrome Beta.app/Contents/MacOS/Google Chrome Beta"

# Environment variable for llvm
export LDFLAGS="-L/usr/local/opt/llvm/lib"
export CPPFLAGS="-I/usr/local/opt/llvm/include"

# environment variable for Golang
export GOPATH=$(go env GOPATH)
# export GOPATH=$HOME/Workspace/Golang
# export GO111MODULE=on
# export GOBIN=${GOPATH//://bin:}/bin

# export SNDCPY_HOME="$HOME/Applications/Android/sndcpy"
# export SNDCPY_APK="$HOME/Applications/Android/sndcpy/sndcpy.apk"

export SNDCPY_HOME="$HOME/Library/sndcpy-v1.1"
export SNDCPY_APK="$HOME/Library/sndcpy-v1.1/sndcpy.apk"
export VLC="/Applications/VLC.app/Contents/MacOS/VLC"

export PYTHON_PATH=$(which python)

# Environment variable for PATH
# export PATH=/usr/local/Cellar/git/2.19.0_2/bin:$PATH
export PATH=$HOME/.nodebrew/current/bin:$PATH
export PATH=$HOME/anaconda3/bin:$PATH
export PATH=$HOME/Repositories/dotfiles/tmux/bin:$PATH
export PATH=$HOME/Library/Flutter/bin:$PATH
export PATH=$HOME/.fzf/bin:$PATH
export FZF_DEFAULT_COMMAND='rg --files --hidden --glob "!.git"'
export FZF_DEFAULT_OPTS='--height 30% --border'
export PATH=$HOME/Library/Android/sdk/platform-tools:$PATH
export PATH=/usr/local/opt/llvm/bin:$PATH
export PATH=/opt/homebrew/bin:$PATH
export PATH=/opt/X11/bin/:$PATH
export PATH=$SNDCPY_HOME/:$PATH
export PATH=$GOPATH/bin:$PATH

export PATH=$PATH:$GOPATH:bin

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

# PS1 setteings
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

# Alias
alias vim='nvim'
alias tmux='tmux -u2'
# alias nvim='~/Library/nvim-macos/bin/nvim'
alias sndcpy="sh sndcpy"
alias scrcpy="scrcpy --turn-screen-off --always-on-top"

# Auto run tmux command when terminal is start at first time
# count=`ps aux | grep tmux | grep -v grep | wc -l`
# if test $count -eq 0; then
#   echo `tmux`
# elif test $count -eq 1; then
#   echo `tmux a`
# fi

fortune | cowsay -f tux
