#! /usr/bin/env bash

####
# Environment setup for macOS
###

## Summary
# 1. Install Homebrew
# 2. Install commandline utilities using Homebrew
# 3. Install OpenJDK from AdoptOpenJDK

###
# 1. Install brew
###

if which brew > /dev/null 2>&1; then
    echo "Homebrew has been alredy installed."
else
    xcode-select --install
    /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
    source $HOME/.bash_profile
    brew doctor
fi

###
# 2. Install commandline utilities using Homebrew
###
brew install git\
    && brew install vim\
    && brew install wget\
    && brew install tmux\
    && brew install nkf\
    && brew install nodebrew\
    && brew install python3\
    && brew install go

echo "Commandline utilities has been installed. Here is the summary."
echo "Install:"
echo "git, vim , wget, tmux, nkf, nodebrew, python3, go"

echo "Note: If you using the node.js, please run following commands;"
echo "\$: nodebrew install-binary latest"
echo "\$: nodebrew list"
echo "\$: nodebrew use <NODE_VERSION>"

###
# 3. Install OpenJDK from AdoptOpenJDK
###

cd $HOME/Downloads
wget https://github.com/AdoptOpenJDK/openjdk12-binaries/releases/download/jdk-12%2B33/OpenJDK12U-jdk_x64_mac_hotspot_12_33.pkg
open OpenJDK12U-jdk_x64_mac_hotspot_12_33.pkg

echo "OpenJDK has been installed."

echo "Setup for macOS has been compleated."
