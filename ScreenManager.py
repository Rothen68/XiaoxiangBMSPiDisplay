#!/usr/bin/env python3.5
#-*- coding: utf-8 -*-

#oled : https://github.com/IOT-MCU/IIC-Pi-OLED/wiki
#enable i2c : https://www.raspberrypi-spy.co.uk/2014/11/enabling-the-i2c-interface-on-the-raspberry-pi/

import board
import digitalio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306


#Used to store gauge information, max 3 gauges
class Gauge:
    def __init__(self, position, value, maxVal=100, minVal=0, char=""):
        self.position = position
        self.newValue = value
        self.currentValue=minVal
        self.maxVal=maxVal
        self.minVal=minVal
        self.char = char



class ScreenManager:

    listGauges = []

    def __init__(self,police, size):
        i2c = board.I2C()
        self.font = ImageFont.truetype(police, size)
        self.oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)
        self.oled.fill(0)
        self.oled.show()
        

    def CleanScreen(self):
        self.oled.fill(0)
        self.oled.show()

    def DrawText(self,text, position = (0,0)):
        image = Image.new("1", (self.oled.width, self.oled.height))
        draw = ImageDraw.Draw(image)
        draw.multiline_text(position,text,font=self.font,fill=255)
        self.oled.image(image)
        self.oled.show()

    def AddGauge(self, position ,value , max=100, min=0, char=''):
        self.listGauges.append(Gauge(position,value,max,min,char))

    def RemoveGauge(self,position):
        for gauge in self.listGauges:
            if gauge.position == position:
                self.listGauges.remove(gauge)


    def SetGaugeValue(self,position,value):
        for gauge in self.listGauges:
            if gauge.position == position:
                if gauge.currentValue != value:
                    gauge.newValue = value                    
                    gauge.currentValue = gauge.newValue

    def DrawGauges(self):
        image = Image.new("1", (self.oled.width, self.oled.height))

        for gauge in self.listGauges:
            self.drawGauge(image,gauge.position,len(self.listGauges),gauge.newValue,gauge.maxVal,gauge.minVal,gauge.char)

        self.oled.image(image)
        self.oled.show()


    def drawGauge(self,image, position, nbrOfGauges ,value , max=100, min=0, char=''):
        draw = ImageDraw.Draw(image)
        width=int(60/nbrOfGauges)
        letterWidth = int(64/nbrOfGauges)
        gX1 = 2
        gY1 = 2+width*position
        gX2 = 109
        gY2 = gY1+width-8
        vX1 = gX2 - (gX2-gX1)*(value-min)/(max-min)
        draw.rectangle([gX1,gY1,gX2,gY2],fill=0,outline=255, width=1)
        draw.rectangle([vX1,gY1,gX2,gY2],fill=255,outline=255)

        #rotate char for vertical display
        txt = Image.new('1',(127-112,32))
        d =ImageDraw.Draw(txt)
        d.text((0,2),char,font=self.font,fill=255)
        w = txt.rotate(90)
        image.paste(w,[112,letterWidth*position,127,letterWidth*position+letterWidth])

    
    