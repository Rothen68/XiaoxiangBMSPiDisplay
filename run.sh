#!/bin/bash

parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
cd "$parent_path"
echo "$parent_path"
echo $PWD
sudo ./bluepy-helper 1
sudo python3 BMS_Display.py > cronLog.txt 2> cronErr.txt