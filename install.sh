#!/bin/bash

#This script will install all the required libraries and register the script to start automatically on pi start

echo "Updating apt"
sudo apt-get update && apt-get upgrade -y

echo "Installing Python and libraries"
sudo apt-get install python3 python3-pip libglib2.0-dev
sudo pip3 install bluepy
sudo pip3 install --upgrade setuptools

mkdir tmp
cd tmp
git clone https://github.com/adafruit/Adafruit_Python_SSD1306.git
cd Adafruit_Python_SSD1306
sudo python setup.py install

cd ..
cd ..
rm -rf tmp

echo ""
echo "    Configure Startup"
echo "sudo bash $PWD/run.sh" | sudo tee -a /etc/profile
echo "Check if /etc/profil contains the previous line"