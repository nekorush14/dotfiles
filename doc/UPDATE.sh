#!/bin/bash

## Copyright (c) 2014, 2016, Mitsuhiro Komuro . All rights reserved.

echo ======================Update Repository ===========================

#Update the repository
sudo apt-get update
if [ $? -ne 0 ]; then 
   echo \>\>Repository update failed. So you mast check package
fi

echo ========================Upgrade Package============================

#Update package
sudo apt-get upgrade
if [ $? -ne 0 ]; then 
   echo \>\>Pakage upgrade failed.
   exit;
fi

echo =========================Remove garbage============================

#Remove garbage
sudo apt-get autoremove

echo ===================================================================
