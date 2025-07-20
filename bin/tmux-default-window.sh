#!/usr/bin/env bash

set -e

tmux split-window -h -l 25%
tmux select-pane -L
tmux split-window -v -l 25%
tmux select-pane -U
