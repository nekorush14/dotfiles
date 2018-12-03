#! /usr/bin/env bash

#########
### Setup the environment
#########

####
## functions
####

path=$(cd $(dirname $0) && pwd)

slink() {
  if [ ! -e $path/$1 ];then
    echo "$path/$1 not exists"
    return 1
  fi
  if remove_file_or_check_link $2/$(basename $1);then
    ln -s $path/$1 $2/$(basename $1)
    echo "$(basename $1) was deployed to $2/"
    return 0
  else
    return 1
  fi
}

#################

####
# General settings
####
slink tmux/.tmux.conf $HOME
slink .gitconfig $HOME
slink .vimrc $HOME

####
## OS dependented bashrc
####
if [[ "$(uname)" = 'Darwin' ]]
then
  slink bashrcs/mac/.bash_profile $HOME
  slink bashrcs/mac/.bashrc $HOME

elif [[ "$(uname)" = 'Linux' ]]
then
  slink bashrcs/linux/.bashrc $HOME

elif [[ "$(uname -r)" =~ ^.*-Microsoft$ ]]
then
  slink bashrcs/wsl/.bashrc $HOME
fi