#!/bin/bash

# Install brew-file package
brew update
brew install brew-file

# Link Brewfile
ln -s ./Brewfile ~/.config/brewfile/Brewfile

# Bundled install brew packages
brew file install
