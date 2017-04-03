#!/bin/bash

#if [ $# -ne 1 ]; then
#  echo "Illegal arguments format."
#  echo "Shell script stoped."
#  exit -1
#fi

PATH=$1

#if [ ${PATH} -eq "~/shellsrc" ] then
#	echo "Can't running script"
#	exit -1
#fi

cd ${PATH}

# Initialize the git status.
/usr/bin/git init

# Initialize the push config.
/usr/bin/git config --global push.dafault simple

# Change the git editor to vim.
/usr/bin/git config --global core.editor "vim"

# Registration my name.
/usr/bin/git config --global user.name "Mitsuhiro Komuro"

# Registration my e-mail address.
/usr/bin/git config --global user.email applemitkom@gmail.com

echo "Git initializeing has been compleated."
echo ""
echo If you need to push remote repository,
echo you should type follow command.\n
echo 1. git remote add origin git@yourRepository
echo 2. git push -u origin master
