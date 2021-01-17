#!/usr/bin/env python3.5
#-*- coding: utf-8 -*-

#python ble scanner library, install : https://elinux.org/RPi_Bluetooth_LE#Using_Bluetooth_LE_with_Python
#github ble scanner : https://ianharvey.github.io/bluepy-doc/scanner.html

import ScreenManager

import time
from bluepy.btle import Scanner, DefaultDelegate, Peripheral

class NotificationDelegate(DefaultDelegate):

    firstPackage = None
    secondPackage = None
    firstNotification = True

    def __init__(self,screen):
        DefaultDelegate.__init__(self)
        self.screen = screen

    def handleNotification(self, cHandle, data):
        #print("notification received : ",data, " handle : ", cHandle)
        self.parseData(data)

    def twoBytesIntoInt(self,highByte, lowByte):
        result = highByte
        result = result << 8
        result = result | lowByte
        return result
        
    def parseData(self,data):
        if (data[0] == 0xdd ):
            self.firstPackage = data
            

        else:
            self.secondPackage = data

        if (self.firstPackage != None and self.secondPackage !=None):
            if(self.firstNotification):
                self.firstNotification=False
                self.screen.CleanScreen()
            data = self.firstPackage + self.secondPackage
            #  0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19    20 21 22 23 24 25 26 27 28 29 30 31 32 33
            # dd 03 00 1b 13 78 00 00 07 ce 07 d0 00 00 28 64 00 00 00 00 // 00 00 21 64 03 0c 02 0b 7a 0b 76 fb a6 77
            if(len(data)==34):
                volts = self.twoBytesIntoInt(data[4],data[5]) *10
                amps = self.twoBytesIntoInt(data[6],data[7]) /100
                remainCapacity = self.twoBytesIntoInt(data[8],data[9])
                percentageRemainCapacity = data[23]
                version = data[22]
                temp1 = (self.twoBytesIntoInt(data[27],data[28]) - 2731)/10
                temp2 = (self.twoBytesIntoInt(data[29],data[30]) - 2731)/10
                print("Volts : ", volts, ", percentage : ", percentageRemainCapacity)
                self.screen.SetGaugeValue(0,volts)
                self.screen.SetGaugeValue(1,percentageRemainCapacity)
                self.screen.DrawGauges()
            self.firstPackage = self.secondPackage = None

def scan(name):
    scanner = Scanner()
    devices = scanner.scan(3)

    for dev in devices:
        print( "Device %s (%s), RSSI=%d dB" % (dev.addr, dev.addrType, dev.rssi))
        for (adtype, desc, value) in dev.getScanData():
            print ("  %s = %s" % (desc, value))
            if(desc == "Complete Local Name" and value == name):
                return dev 
    return None 
                


screen = ScreenManager.ScreenManager("Roboto-Regular.ttf", 20)
screen.DrawText("BMS Display \nSearching...")
screen.AddGauge(0,0,50000,43200,"V")
screen.AddGauge(1,0,char="P")


deviceInfo = scan("xiaoxiang BMS")

if(deviceInfo !=None):
    screen.DrawText("BMS found :  \n" + deviceInfo.addr + "\nConnecting ...")
    print("addr : %s\naddrType : %s" %(deviceInfo.addr,deviceInfo.addrType))
    for (adtype, desc, value) in deviceInfo.getScanData():
        print ("  %s = %s" % (desc, value))
    device = Peripheral(deviceInfo)
    notificationDelegate = NotificationDelegate(screen)
    device.setDelegate(notificationDelegate)
    services = device.getServices()
    rxCharacteristic = None #Stores characteristic to read BMS data
    txCharacteristic = None #Stores characteristic to write BMS data
    for service in services:
        characteristics = service.getCharacteristics()
        for characteristic in characteristics:
            if(service.uuid == "0000ff00-0000-1000-8000-00805f9b34fb" and characteristic.uuid == "0000ff01-0000-1000-8000-00805f9b34fb"):
                rxCharacteristic = characteristic
            if(service.uuid == "0000ff00-0000-1000-8000-00805f9b34fb" and characteristic.uuid == "0000ff02-0000-1000-8000-00805f9b34fb"):
                txCharacteristic = characteristic
    if(txCharacteristic != None and rxCharacteristic != None):
        array =bytes.fromhex("dd a5 03 00 ff fd 77")
        while notificationDelegate.firstNotification:
            txCharacteristic.write(array,True)
        while True:
            txCharacteristic.write(array,True)
            time.sleep(2)

