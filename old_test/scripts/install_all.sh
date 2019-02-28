#!/bin/bash

PACKAGES="build-essential zip unzip ssh git python3 python3-pip python3-pyqt5 pyzo gconf-service gconf-service-backend gconf2 gconf2-common git-man gvfs-bin libcurl3 liberror-perl libgconf-2-4"

yes | sudo apt-get update
yes | sudo apt-get upgrade
yes | sudo apt-get autoremove

yes | sudo apt-get install $PACKAGES

wget -q --show-progress https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
sudo bash Miniconda3-latest-Linux-x86_64.sh
rm Miniconda3-latest-Linux-x86_64.sh

wget -q --show-progress --output-document=atom.deb https://atom.io/download/deb
yes | sudo dpkg -i atom.deb
yes | sudo apt-get install --fix-broken
rm atom.deb

sudo -H python3 -m pip install --upgrade pip
sudo -H python3 -m pip install numpy matplotlib tensorflow pillow PyQt5
