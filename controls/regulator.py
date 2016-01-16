#!/usr/bin/env python3

# Reads output of thermometer.py and controls the relay to regulate temperature.
# Reprints streamed stdout from thermometer.py. Everything else goes to stderr.

import sys
import datetime
import RPi.GPIO as GPIO

pin = 17
usage = 'Usage: {} <lower_bound_C> <upper_bound_C>'.format(sys.argv[0])

def ts():
    return datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')

def fail(msg):
    print(msg, file=sys.stderr, flush=True)
    exit(1)

if len(sys.argv) != 3:
    fail(usage)

try:
    lower = float(sys.argv[1])
    upper = float(sys.argv[2])
except ValueError:
    fail('lower and upper bounds must be numbers')
if lower >= upper:
    fail('lower bound must be less than upper bound')

GPIO.setmode(GPIO.BCM)
GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)
try:
    while True:
        line = sys.stdin.readline().strip()
        print(line, flush=True)
        # line format is: timestamp[tab]degrees_c[tab]degrees_f
        c = float(line.split('\t')[1])
        if c <= lower:
            msg = '{} <= {}\tpower off'.format(c, lower)
            print(ts(), msg, file=sys.stderr, flush=True)
            GPIO.output(pin, GPIO.LOW)
        elif c >= upper:
            msg = '{} >= {}\tpower on'.format(c, upper)
            print(ts(), msg, file=sys.stderr, flush=True)
            GPIO.output(pin, GPIO.HIGH)
finally:
    print(ts(), 'cleaning up GPIO', file=sys.stderr, flush=True)
    GPIO.cleanup()
