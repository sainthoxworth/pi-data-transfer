# -*- coding: utf-8 -*-


# ------------------------------------------------------------------------

#python
# To run code use: python upload-json-file-to-firestore.py data.json add users-demo-add
# for command line arguements.
import sys
import json

# SETTING UP YOUR VIRTUAL ENVIRONMENT
# For Mac
# pip install virtualenv
# virtualenv <your-env>
# source tutoring/bin/activate
# tutoring/bin/pip install google-cloud-firestore

# For Window
# pip install virtualenv
# virtualenv <your-env>
# <your-env>\Scripts\activate
# <your-env>\Scripts\pip.exe install google-cloud-firestore

import timeit
import RPi.GPIO as GPIO
import time

import serial               #import serial pacakge
from time import sleep
import webbrowser           #import package for opening link in browser
import sys                  #import system package

def GPS_Info():
    global NMEA_buff
    global lat_in_degrees
    global long_in_degrees
    nmea_time = []
    nmea_latitude = []
    nmea_longitude = []
    nmea_time = NMEA_buff[0]                    #extract time from GPGGA string
    nmea_latitude = NMEA_buff[1]                #extract latitude from GPGGA string
    nmea_longitude = NMEA_buff[3]               #extract longitude from GPGGA string
    
    print("NMEA Time: ", nmea_time,'\n')
    print ("NMEA Latitude:", nmea_latitude,"NMEA Longitude:", nmea_longitude,'\n')
    
    lat = float(nmea_latitude)                  #convert string into float for calculation
    longi = float(nmea_longitude)               #convertr string into float for calculation
    
    lat_in_degrees = convert_to_degrees(lat)    #get latitude in degree decimal format
    long_in_degrees = convert_to_degrees(longi) #get longitude in degree decimal format
    
#convert raw NMEA string into degree decimal format   
def convert_to_degrees(raw_value):
    decimal_value = raw_value/100.00
    degrees = int(decimal_value)
    mm_mmmm = (decimal_value - int(decimal_value))/0.6
    position = degrees + mm_mmmm
    position = "%.4f" %(position)
    return position
    


gpgga_info = "$GPGGA,"
ser = serial.Serial ("/dev/ttyS0")              #Open port with baud rate
GPGGA_buffer = 0
NMEA_buff = 0
lat_in_degrees = 0
long_in_degrees = 0

try:
    while True:
        received_data = (str)(ser.readline())                   #read NMEA string received
        GPGGA_data_available = received_data.find(gpgga_info)   #check for NMEA GPGGA string
        if (GPGGA_data_available>0):
            GPGGA_buffer = received_data.split("$GPGGA,",1)[1]  #store data coming after "$GPGGA," string 
            NMEA_buff = (GPGGA_buffer.split(','))               #store comma separated data in buffer
            GPS_Info()                                          #get time, latitude, longitude
 
            print("lat in degrees:", lat_in_degrees," long in degree: ", long_in_degrees, '\n')
#            map_link = 'http://maps.google.com/?q=' + lat_in_degrees + ',' + long_in_degrees    #create link to plot location on Google map
            print("<<<<<<<<press ctrl+c to plot location on google maps>>>>>>\n")               #press ctrl+c to plot on map and exit 
            print("------------------------------------------------------------\n")
                        
except KeyboardInterrupt:
#    webbrowser.open(map_link)        #open current position information in google map
    sys.exit(0)

GPIO.setmode(GPIO.BCM)

TRIG = 23
ECHO = 24

print ("Distance Measurement in progress...")

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

GPIO.output(TRIG, False)

print ("Waiting For Sensor")
time.sleep(2)

GPIO.output(TRIG, True)
time.sleep(0.00001)

GPIO.output(TRIG, False)

while GPIO.input(ECHO)==0:
    pulse_start = time.time()

while GPIO.input(ECHO)==1:
    pulse_end = time.time()
    

pulse_duration = pulse_end - pulse_start

distance = pulse_duration * 17150
distance = round(distance, 2)

print ("Distance: " + distance + "cm")

GPIO.cleanup()

uploadjson = UploadJsonFileToFirestore()
uploadjson.upload()      
