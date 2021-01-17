# XiaoxiangBMSPiDisplay

# Step 1 : Install Raspberry Pi OS Lite (32-Bit)

# Step 2 : configuring the rPi 
On the SD card
 - add an empty ssh file on boot
 - add a wpa_supplicant.conf file : 
 ```
  country=US # Your 2-digit country code
  ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
  network={
      ssid="YOUR_NETWORK_NAME"
      psk="YOUR_PASSWORD"
      key_mgmt=WPA-PSK
  }
  ```
Then run the pi
 - connect to ssh
 - change pi user password with passwd command
 - copy content from github on the pi
 - navigate to the folder 
  - run ```sudo raspi-config```
    - enable i2c in "Interface Options"
    - enable auto login in "System Options"
 - run ```sudo bash install.sh```
 - take a coffee
 - add the line to /etc/profil by ```sudo nano /etc/profile``` : 
 ```sudo bash /home/pi/$$Folder$$/run.sh```

 



