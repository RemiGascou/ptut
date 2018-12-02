#!/bin/bash

basedir="apps"
cd ../
cd $basedir

for subdir in $(ls -d */); do
    echo -e "\x1b[1m[\x1b[92mcleaning\x1b[0m\x1b[1m] $subdir\x1b[0m"
    cd $subdir
    cd lib/
    for dir in $(find ./ -mindepth 1 -type d); do
    	if [[ $dir == *"__pycache__" ]]; then
    		echo -e "\x1b[1m[\x1b[93mremoving\x1b[0m\x1b[1m] $dir\x1b[0m"
    		rm -rf $dir
    	fi
    done
    cd ../../
done
