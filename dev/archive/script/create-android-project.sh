#!/usr/bin/env bash

MULTIM="--multimodule"

# exit when any command fails
set -e

# Check arguments
if [[ $# -lt 2 ]]; then
   echo "Usage: bash create-android-project.sh my.new.package MyNewDataModel [ApplicationName] [--multimodlue]" >&2
   exit 2
fi

PACKAGE=$1
DATAMODEL=$2
APPNAME=$3
SUBDIR=${PACKAGE//.//} # Replaces . with /
CURRENTDIR=$(pwd}
TYPENAME=$4

if [ "$TYPENAME" != "$MULTIM" ]; then
  echo "Usage: bash create-android-project.sh my.new.package MyNewDataModel [ApplicationName] [--multimodlue]" >&2
  exit 3
fi

# Clone template project
if [[ $TYPENAME ]] then
  git clone https://github.com/android/architecture-templates.git --branch multimodule $APPNAME
else
  git clone https://github.com/android/architecture-templates.git --branch base $APPNAME
fi

echo "Clone: Done!"

cd ./$APPNAME

# Configure project
if [[ $APPNAME ]] then
  bash customizer.sh $PACKAGE $DATAMODEL $APPNAME
else
  bash customizer.sh $PACKAGE $DATAMODEL
fi

echo "Project configration: Done!"

# Initialize the git
git init
git add .
git commit -m "Initial commit"

echo "Git settings: Done!"

cd $CURRENTDIR

echo "Android project setup: Completed!"

