#!/usr/bin/python

import RPi.GPIO as GPIO
import spidev
import time
import decimal,mail
import os,ultrasonic,sms

GPIO.setmode(GPIO.BCM)

GPIO.setup(16,GPIO.OUT)  #Motor1
GPIO.setup(20,GPIO.OUT)  #MOTOR2
GPIO.setwarnings(False)


GPIO.setup(12, GPIO.IN)

# Open SPI bus
spi = spidev.SpiDev()
spi.open(0,0)
 
# Function to read SPI data from MCP3008 chip
# Channel must be an integer 0-7
def ReadChannel(channel):
  adc = spi.xfer2([1,(8+channel)<<4,0])
  data = ((adc[1]&3) << 8) + adc[2]
  return data
 
# Function to convert data to voltage level,
# rounded to specified number of decimal places.
def ConvertVolts(data,places):
  volts = (data * 3.3) / float(1023)
  volts = round(volts,places)
  return volts
 
# Function to calculate temperature from
# TMP36 data, rounded to specified
# number of decimal places.
def ConvertTemp(data,places): 
 
  temp = ((data * 330)/float(1023))
  temp = round(temp,places)
  temp = temp *0.5

  return temp
 
# Define sensor channels
x_channel  = 0

z_channel= 2
x1_channel=3



 
# Define delay between readings


while True:
  
  
  # Read the temperatuj re sensor data
  X_level = ReadChannel(x_channel)
  X = ConvertTemp(X_level,2)
  print 'Temperature', X
  distance= ultrasonic.ultra()
  print 'distance=',distance
  Z_level = ReadChannel(z_channel)
  Z = ConvertTemp(Z_level,2)
  
  print 'LEVEL',Z

  
  x1_level = ReadChannel(x1_channel)
  x1 = ConvertTemp(x1_level,2)  
  print 'Moisture',x1
  
  if(GPIO.input(12)==1):
    print'intruder detection'
    mail.main("therisudhu123@gmail.com",'rohitviratsudhu12345','hbkvignesh.d@gmail.com')
    sms.msg("9944655660",'F3924D','intruder detected','9944655660')
  
  
  if(x1>150):
        GPIO.output(16,True)
        sms.msg("9944655660",'F3924D','Soil is dry','9944655660')
  else:
        GPIO.output(16,False)
        
  if(Z<50):
        GPIO.output(20,True)
        sms.msg("9944655660",'F3924D','water level is low','9944655660')
               
  
  else:
        GPIO.output(20,False)
        
  data='temperature'+str(X)+'Water Level'+str(Z)+'Moisture'+str(x1)
  f=open('/home/pi/log.txt','w')
  f.write(data)
  f.close()

  
       
