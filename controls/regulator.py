#!/usr/bin/env python3

# Reads output of thermometer.py and controls the relay to regulate temperature.
# Reprints streamed stdout from thermometer.py. Everything else goes to stderr.

import sys
import datetime
import RPi.GPIO as GPIO

usage = 'Usage: {} <lower_bound_C> <upper_bound_C>'.format(sys.argv[0])
pin = 17
initial = GPIO.LOW

def stderr(*messages):
    ts = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
    print(ts + '\t' + '\t'.join(messages), file=sys.stderr, flush=True)

if len(sys.argv) != 3:
    stderr(usage)
    exit(1)

try:
    lower = float(sys.argv[1])
    upper = float(sys.argv[2])
except ValueError:
    stderr('lower and upper bounds must be numbers')
    exit(1)
if lower > upper:
    stderr('lower bound cannot be greater than upper bound')
    exit(1)

GPIO.setmode(GPIO.BCM)
GPIO.setup(pin, GPIO.OUT, initial=initial)
state = initial
try:
    stderr('starting regulator')
    while True:
        line = sys.stdin.readline()
        print(line, end='', flush=True) # re-echo stdin to stdout

        # line format is: timestamp[tab]degrees_c[tab]degrees_f
        c = float(line.split('\t')[1])
        if c <= lower and state == GPIO.HIGH:
            stderr('{} <= {}'.format(c, lower), 'power off')
            GPIO.output(pin, GPIO.LOW)
            state = GPIO.LOW
        elif c >= upper and state == GPIO.LOW:
            stderr('{} >= {}'.format(c, upper), 'power on')
            GPIO.output(pin, GPIO.HIGH)
            state = GPIO.HIGH
except KeyboardInterrupt:
    pass # don't show stacktrace on ctrl-c
finally:
    stderr('stopping regulator')
    GPIO.cleanup()
