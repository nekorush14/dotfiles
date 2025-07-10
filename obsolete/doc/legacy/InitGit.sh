#!/bin/bash

PATH=$1

cd ${PATH}

# Initialize the git status.
/usr/bin/git init

# Initialize the push config.
/usr/bin/git config --global push.dafault simple

# Change the git editor to vim.
/usr/bin/git config --global core.editor "vim"

echo "Git initializeing has been compleated."
echo ""
echo You need to setup the Git global user name and email address.
echo If you need to push remote repository,
echo you should type follow command.\n
echo 1. git remote add origin git@yourRepository
echo 2. git push -u origin master
