#!/usr/bin/env python3

# Outputs temperature readings at regular intervals.
# Data is printed to stdout. Everything else goes to stderr.
# stdout format is: timestamp[tab]degrees_c[tab]degrees_f

# More info about the driver for the temperature sensor at
# https://www.kernel.org/doc/Documentation/w1/slaves/w1_therm
# Datasheet at http://cdn.sparkfun.com/datasheets/Sensors/Temp/DS18B20.pdf

import glob
import time
import sys
import datetime

retry = 4  # how many seconds to wait for retry on checksum mismatch
usage = 'Usage: {} <interval_seconds> [w1_file]'.format(sys.argv[0])

def ts():
    return datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')

def fail(msg):
    print(msg, file=sys.stderr, flush=True)
    exit(1)

if len(sys.argv) not in (2,3):
    fail(usage)

try:
    interval = int(sys.argv[1])
except ValueError:
    fail('interval must be an integer')
if interval <= 0:
    fail('interval should be > 0')

if len(sys.argv) == 3:
    device_file = sys.argv[2]
else:
    # try to automatically look up the file
    dir_pattern = '/sys/bus/w1/devices/28*'
    dir_glob = glob.glob(dir_pattern)
    if len(dir_glob) != 1:
        fail('found {} matching dirs for {}'.format(len(dir_glob),dir_pattern))
    device_file = dir_glob[0] + '/w1_slave'


try:
    while True:
        with open(device_file, 'r') as f:
            line = f.readline().strip()
            if line[-3:] != 'YES':
                msg = 'crc checksum mismatch; retrying in {}s'.format(retry)
                print(ts(), msg, file=sys.stderr, flush=True, sep='\t')
                time.sleep(retry)
                continue

            line = f.readline().strip()
            t_index = line.find('t=')
            t_millidegrees = float(line[t_index+2:])
            t_c = t_millidegrees / 1000.0
            t_f = t_c * 9.0 / 5.0 + 32.0
            print(ts(), t_c, t_f, sep='\t', flush=True)
        time.sleep(interval)
except KeyboardInterrupt:
    pass # don't show stacktrace on ctrl-c
finally:
    print(ts(), 'stopping thermometer', flush=True, sep='\t', file=sys.stderr)
