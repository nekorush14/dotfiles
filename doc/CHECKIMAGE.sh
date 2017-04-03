#!/bin/bash

echo ===================Current Linux image======================

#Display current using linux image
uname -sorpo

echo ==================Installed Linux image=====================

#Check current installed linux image
dpkg --get-selections | grep linux-image

echo ===============Remove Linux image command===================

#Display remove command
echo sudo apt-get autoremove --purge linux-image-x.x.x-xx-generic

echo ============================================================
