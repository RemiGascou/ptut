#!/bin/bash

PACKAGES="ssh python3 python3-pyqt5 python3-pip pyzo"
PYTHONLIBS="numpy pillow tensorflow PyQt5"


if [ "$(id -u)" != "0" ]; then
	echo "You need to be root to run this script. Try \"sudo\""
	exit 1
fi


echo -e "\x1b[1m[\x1b[92m***install***\x1b[0m\x1b[1m]\x1b[0m Installing packages : \x1b[1m$PACKAGES\x1b[0m"
yes | sudo apt-get install python3 python3-pyqt5 python3-pip pyzo
echo -e "\x1b[1m[\x1b[92mpython3--libs\x1b[0m\x1b[1m]\x1b[0m Upgrading pip"
yes | sudo -H python3 -m pip install --upgrade pip
echo -e "\x1b[1m[\x1b[92mpython3--libs\x1b[0m\x1b[1m]\x1b[0m Installing python libraries : \x1b[1m$PYTHONLIBS\x1b[0m"
yes | sudo python3 -m pip install $PYTHONLIBS
