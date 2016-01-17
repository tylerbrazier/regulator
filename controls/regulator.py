#!/usr/bin/env python3

# Reads output of thermometer.py and controls the relay to regulate temperature.
# Reprints streamed stdout from thermometer.py. Everything else goes to stderr.

import sys
import datetime
import RPi.GPIO as GPIO

usage = 'Usage: {} <lower_bound_C> <upper_bound_C>'.format(sys.argv[0])
pin = 17
initial = GPIO.LOW

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
if lower > upper:
    fail('lower bound must be less than upper bound')

GPIO.setmode(GPIO.BCM)
GPIO.setup(pin, GPIO.OUT, initial=initial)
state = initial
try:
    while True:
        line = sys.stdin.readline()
        print(line, end='', flush=True) # re-echo stdin to stdout

        # line format is: timestamp[tab]degrees_c[tab]degrees_f
        c = float(line.split('\t')[1])
        if c <= lower and state == GPIO.HIGH:
            msg = '{} <= {}'.format(c, lower)
            print(ts(), msg, 'power off', file=sys.stderr, flush=True, sep='\t')
            GPIO.output(pin, GPIO.LOW)
            state = GPIO.LOW
        elif c >= upper and state == GPIO.LOW:
            msg = '{} >= {}'.format(c, upper)
            print(ts(), msg, 'power on', file=sys.stderr, flush=True, sep='\t')
            GPIO.output(pin, GPIO.HIGH)
            state = GPIO.HIGH
except KeyboardInterrupt:
    pass # don't show stacktrace on ctrl-c
finally:
    print(ts(), 'stopping regulator', file=sys.stderr, flush=True, sep='\t')
    GPIO.cleanup()
