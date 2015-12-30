#!/usr/bin/env python3

import glob
import time
import sys
import datetime

# Outputs temperature readings at regular intervals.
# Data is printed to stdout. Everything else goes to stderr.

# More info about the driver for the temperature sensor at
# https://www.kernel.org/doc/Documentation/w1/slaves/w1_therm
# Datasheet at http://cdn.sparkfun.com/datasheets/Sensors/Temp/DS18B20.pdf

def stderr(msg):
    print(msg, file=sys.stderr)

def fail():
    stderr('Usage: {} <interval_seconds>'.format(sys.argv[0]))
    exit(1)


if len(sys.argv) != 2:
    fail()

try:
    interval = int(sys.argv[1])
except ValueError:
    fail()


retry_delay = 1  # how long to wait for retry if something goes wrong
device_file = glob.glob('/sys/bus/w1/devices/28*')[0] + '/w1_slave'

def ts():
    return datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')

def retry(msg):
    stderr('{} {}; retrying in {}s'.format(ts(), msg, retry_delay))
    time.sleep(retry_delay)


f = open(device_file)
stderr('Timestamp\t\tC\tF')
while True:
    try:
        f.seek(0)
        line = f.readline().strip()
        if line[-3:] != 'YES':
            retry('crc checksum mismatch')
            continue

        line = f.readline().strip()
        t_index = line.find('t=')
        if t_index < 0:
            retry("no 't=' in '{}'".format(line))
            continue

        t_str = line[t_index+2:]
        try:
            t_millidegrees = float(t_str)
        except ValueError:
            retry("failed to parse number from '{}'".format(t_str))
            continue

        t_c = t_millidegrees / 1000.0
        t_f = t_c * 9.0 / 5.0 + 32.0
        print(ts(), t_c, t_f, sep='\t')
        time.sleep(interval)

    except KeyboardInterrupt:
        break

f.close()

