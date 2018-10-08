#!/usr/bin/env python

import commands
import RPi.GPIO as GPIO
from time import sleep

BUTTON_WIFI = 20

LED_WIFI = 26

WAIT_TIME = 0.5

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_WIFI, GPIO.OUT)
GPIO.setup(BUTTON_WIFI, GPIO.IN) 

cnt = 0

try:
    while True:
        if GPIO.input(BUTTON_WIFI) == GPIO.HIGH:
            GPIO.output(LED_WIFI, GPIO.HIGH)
            cnt += WAIT_TIME
            if cnt >= 5:
                commands.getoutput("echo 1 > /home/pi/raspberrypi-wifi-config-script/wifi-config-sequence")
                commands.getoutput("/home/pi/raspberrypi-wifi-config-script/check-wifi-config-sequence.sh")
        else:
            cnt = 0
            GPIO.output(LED_WIFI, GPIO.LOW)

        sleep(WAIT_TIME)

except KeyboardInterrupt:
    pass

GPIO.cleanup()

