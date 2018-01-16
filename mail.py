from __future__ import print_function
import datetime
import RPi.GPIO as GPIO
import DHT11_Python.dht11 as dht11
import time
import mysql.connector as mysqli
from mysql.connector import errorcode
import Adafruit_DHT as dht22

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.cleanup()

GPIO.setup(7, GPIO.OUT, initial=GPIO.LOW) 
GPIO.setup(11, GPIO.OUT, initial=GPIO.LOW) 
GPIO.setup(13, GPIO.OUT, initial=GPIO.LOW) 
light_state = 0 
humid_state = 0 
reserr_count = 0

instance = dht11.DHT11(pin = 7) 
time.sleep(1) 
GPIO.output(11,0)

while 1:
    dt = datetime.datetime.now()
    dt1 = dt.timetuple()
    dt2 = dt.isoformat()
    
    time.sleep(2)
    h, t = dht22.read(dht22.DHT22,4)
    print(h)
    print(t)
    if h is not None and t is not None:
        if (h < 50) & (humid_state == 0):
            GPIO.output(13,1)
            humid_state = 1
        if (h > 55) & (humid_state == 1):
            GPIO.output(13,0)
            humid_state = 0
    else:
        reserr_count += 1
    # this section response for himidity
    #result = instance.read()
    #time.sleep(2)
    #if result.is_valid():
    #    reserr_count = 0
    #    if (result.humidity < 50) & (humid_state == 0) :
    #        GPIO.output(13,1)
    #        humid_state = 1
    #    if (result.humidity > 55) & (humid_state == 1) :
    #        GPIO.output(13,0)
    #        humid_state = 0 
    #else :
    #    reserr_count += 1
    
    # this section responsible for lighting
    if   (dt1[3] >= 8) & (dt1[3] < 20) :
        if (light_state == 0) :
            GPIO.output(11,1)
            light_state = 1
    else :
        if (light_state == 1) :
            GPIO.output(11,0)
            light_state = 0

    #if result.is_valid():
    if h is not None and t is not None:
        state = ("INSERT INTO hydrostats (temp,humidity,light,humidifier) VALUES ({},{},{},{})")
        cnx = mysqli.connect(user='root', password='ffuswgwy',database='hydropony',host='127.0.0.1')
        cursor = cnx.cursor()
        data = state.format(t,h,light_state,humid_state) 
        cursor.execute(data)
        cnx.commit()
        cursor.close()
        cnx.close()
    time.sleep(15)
