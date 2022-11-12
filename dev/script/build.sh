#! /usr/bin/env bash

# Set Application project
PROJ_PATH="PATH_TO_TARGET_CSPROJ"

# Build msproj
msbuild build.proj

echo "--------------------------------"
echo "Project build has been copleted."
echo "--------------------------------"

# Auto incriment application revision
revision=`grep ApplicationRevision $PROJ_PATH | sed 's/^.*>\(.*\)<.*$/\1/'`
echo "Current app revision: $revision"
((revision++))
echo "Next app revision: $revision"
sed -i "s/ApplicationRevision>\(.*\)<.*$/ApplicationRevision>$revision<\/ApplicationRevision>/g" $PROJ_PATH ## For GNU sed
# sed -i "" "s/ApplicationRevision>\(.*\)<.*$/ApplicationRevision>$revision<\/ApplicationRevision>/g" $PROJ_PATH ## For BSD sed
echo "App revision has been incremented."

echo "------------------------------"
echo "Build task has been completed."
echo "------------------------------"
