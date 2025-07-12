#!/usr/bin/env bash

# install tpm
if type "tmux" >/dev/null 2>&1; then
  git clone https://github.com/tmux-plugins/tpm ~/.tmux/plugins/tpm
fi

# copy custom scripts for tmux
if [ -d $Home/.local/bin ]; then
  cp ./tmux-short-path.sh ~/.local/bin/tmux-short-path.sh
else
  mkdir -p $Home/.local/bin
  cp ./tmux-short-path.sh ~/.local/bin/tmux-short-path.sh
fi

echo "After install tpm plugins, you must edit tmux-weather script manuary to display wind speed by m/s."
echo "Please edit .tmux/plugins/tmux-weather/scripts/weather.sh and add [ \"\$units\" != \"m\" ] condition to original if conditions by AND operator."
