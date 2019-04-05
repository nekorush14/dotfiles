#!/bin/bash

## Copyright (c) 2014, 2017, Mitsuhiro Komuro . All rights reserved.
# Using "apt" command. Please note different package system.

echo ======================Update Repository ===========================

#Update the repository
sudo apt update
if [ $? -ne 0 ]; then 
   echo \>\>Repository update failed. So you mast check package
fi

echo ========================Upgrade Package============================

#Update package
sudo apt upgrade
if [ $? -ne 0 ]; then 
   echo \>\>Pakage upgrade failed.
   exit;
fi

echo =========================Remove garbage============================

#Remove garbage
sudo apt autoremove

echo ===================================================================
