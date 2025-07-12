#!/usr/bin/env bash

# install tpm
if type "tmux" >/dev/null 2>&1; then
  git clone https://github.com/tmux-plugins/tpm ~/.tmux/plugins/tpm
fi
