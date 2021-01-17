#!/bin/bash

#This script will install all the required libraries and register the script to start automatically on pi start

echo "Updating apt"
sudo apt-get update && apt-get upgrade -y

echo "Installing Python and libraries"
sudo apt-get install -y python3 python3-pip libglib2.0-dev libopenjp2-7 libtiff5
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

sudo python3 -m pip3 install --force-reinstall adafruit-blinka
sudo pip3 install --upgrade adafruit-python-shell
sudo pip3 install Pillow
sudo pip3 install adafruit-circuitpython-ssd1306


