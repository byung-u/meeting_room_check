#!/usr/local/bin/python
from __future__ import print_function
from redislite import StrictRedis
from redis_collections import List

import RPi.GPIO as GPIO
import os
import time

__author__ = 'Gus (Adapted from Adafruit)'
__license__ = "GPL"
__maintainer__ = "pimylifeup.com"

GPIO.setmode(GPIO.BOARD)

# define the pin that goes to the circuit
pin_to_circuit = 7


def get_rp_serial():
    try:
        f = open('/proc/cpuinfo', 'r')
        for line in f:
            if line[0:6] == 'Serial':
                cpu_serial = line[10:26]
        f.close()
    except:
        cpu_serial = None

    return cpu_serial


def rc_time(pin_to_circuit):
    count = 0

    # Output on the pin for
    GPIO.setup(pin_to_circuit, GPIO.OUT)
    GPIO.output(pin_to_circuit, GPIO.LOW)
    time.sleep(0.1)  # sec

    # Change the pin back to input
    GPIO.setup(pin_to_circuit, GPIO.IN)

    # Count until the pin goes high
    while (GPIO.input(pin_to_circuit) == GPIO.LOW):
        count += 1
    return count


def redis_init():
    serial_number = get_rp_serial()  # get cpu serial number
    if serial_number is None:
        serial_number = '00000001'  # temp number

    ip = os.environ.get('RS_HOST')  # RS: raspberry pi
    port = os.environ.get('RS_PORT')
    pw = os.environ.get('RS_PASSWORD')

    redis_connection = StrictRedis(host=ip, port=port, db=0, password=pw)
    r = List(redis=redis_connection, key='rp3:'+serial_number)
    return r


# Catch when script is interupted, cleanup correctly
try:
    r = redis_init()
    # Main loop
    while True:
        current_light = rc_time(pin_to_circuit)
        try:
            r.append(current_light)
            print(current_light)
        except Exception as e:
            print("error: ", e)
            pass
        time.sleep(1)  # sec
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()
