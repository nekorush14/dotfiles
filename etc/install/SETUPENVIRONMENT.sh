#!/bin/bash

##########################################################
#               Set up new environment                   #
# Copyright(C) 2016 Mitsuhiro komuro All Rights Reserved #
#                                                        #
# This script set up environment for plean OSs.          #
#                                                        #
# Following software is installed                        #
#                                                        #
#   * Util-app                                           #
#   |  |- lv                                             #
#   |  |- vim                                            #
#   |  |- git                                            #
#   |  |- screenfetch                                    #
#   |  |- unity-tweek-tools                              #
#   |                                                    #
#   * other-app                                          #
#      |- moc                                            #
#      |- w3m                                            #
#      |- w3m-img                                        #
#      |- chromium                                       #
#                                                        #
# Following library will install                         #
#                                                        #
#  * Setting lib                                         #
#  |   |- ttf-mscorefonts                                #
#  |                                                     #
#  * Other lib                                           #
#      |- Oracl-jdk-8                                    #
#                                                        #
# After that, running following commands                 #
#                                                        #
#   * ssh-keygen                                         #
#                                                        #
##########################################################

echo "This system useing \"apt\" command "
echo "Don\'t use \"apt-get\" command "

# PACKAGE Control section #

# update package
sudo apt update

# upgrade package
sudo apt upgrade

# Gabage collection
sudo apt autoremove -n

# End of section #


# Install applications section #
sudo apt install lv vim git screenfetch unity-tweek-tools
sudo apt install moc w3m w3m-img chromium
# End of section #

# Add apt key
sudo add-apt-repository -y ppa:webupd8team/java

# Install library software section #
sudo apt install ubuntu-restricted-extras
sudo apt install oracle-java8-installer
# End of section #

# Running commnad section #
ssh-keygen -t rsa;
sudo sed -i 's/#NTP=/NTP=ntp.nict.jp/g' /etc/systemd/timesyncd.conf;
sudo sh -c 'printf "[SeatDefaults]\nallow-guest=false\n" >/usr/share/lightdm/lightdm.conf.d/50-no-guest.conf';
sudo apt remove unity-webapps-common;
# Setting commands section #


echo ""
echo "================================"
echo "This script has benn compleated."
echo "================================"

