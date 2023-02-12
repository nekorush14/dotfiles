#! /usr/bin/env bash

echo ""
echo "[INFO] WSL package setup v0.1.0"
echo ""

# General config
sudo update-alternatives --set editor /usr/bin/vim.basic

# Update repository source
echo "[INFO] Update package repository to JP >"
sudo sed -i -e 's%http://.*.ubuntu.com%http://ftp.jaist.ac.jp/pub/Linux%g' /etc/apt/sources.list
echo "[INFO] Update package reposiotry: Done"

# Update and upgrade package source
echo "[INFO] Update/Upgrade repository >"
sudo apt update;sudo apt upgrade -y
echo "[INFO] Package update and upgrade: Done"

# Install required packages
echo "[INFO] Install requred packages >"
sudo apt install -y git tmux vim build-essential zsh procps curl file neovim ripgrep bat fd-find duf neofetch w3m w3m-img

git clone https://github.com/zsh-users/zsh-completions.git ~/.zsh/zsh-completions
git clone https://github.com/zsh-users/zsh-autosuggestions ~/.zsh/zsh-autosuggestions
echo "[INFO] apt managed package install: Done"

# Install homebrew
echo "[INFO] Install homebrew >"
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
echo "[INFO] homebrew install: Done"

# Configure homebrew
echo "[INFO] configure homebrew >"
echo '# Set PATH, MANPATH, etc., for Homebrew.' >> $HOME/.profile
echo 'eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"' >> $HOME/.profile
eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"
source $HOME/.bashrc
echo "[INFO] Configure homebrew: Done"

# Install homebrew managed packages
echo "[INFO] Install homebrew managed packages >"
brew install gcc
brew tap tgotwig/linux-dust && brew install dust
brew install procs
brew install jesseduffield/lazygit/lazygit && brew install lazygit
brew install jesseduffield/lazydocker/lazydocker
brew install lsd
brew install bat
brew install glab

echo "[INFO] Install homebrew managed packages: Done"

# Install docker
echo "[INFO] Install docker-ce >"
sudo apt install -y apt-transport-https ca-certificates curl gnupg lsb-release
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo \
  "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt update && sudo apt install -y docker-ce docker-ce-cli containerd.io
echo "[INFO] Install docker-ce: Done"

# Install docker-compose
echo "[INFO] Install docker-compose using homebrew >"
brew install docker-compose
echo "[INFO] Install docker-compose: Done"

# Configure docker for root-less mode
echo "[INFO] Configure docker for root-less mode >"
sudo groupadd docker
sudo usermod -aG docker $USER
sudo bash -c "echo '$USER ALL=NOPASSWD: /usr/sbin/service docker start, /usr/sbin/service docker stop, /usr/sbin/service docker restart' >> /etc/sudoers"
echo "" >> $HOME/.bashrc
echo "service docker status > /dev/null 2>&1" >> $HOME/.bashrc
echo "if [ \$? = 1 ]; then" >> $HOME/.bashrc
echo "    sudo service docker start" >> $HOME/.bashrc
echo "fi" >> $HOME/.bashrc
echo "" >> $HOME/.bashrc
echo "[INFO] Configure docker for root-less mode: Done"
echo ""

# Setup complete
# After setup log messages
echo "[WARN] You need to log out and log back the shell to re-evaluate the group information."
echo ""
echo "[INFO] Package setup: Done"

