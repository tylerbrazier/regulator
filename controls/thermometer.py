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

def stderr(*messages):
    print(ts() + '\t' + '\t'.join(messages), file=sys.stderr, flush=True)

if len(sys.argv) not in (2,3):
    stderr(usage)
    exit(1)

try:
    interval = int(sys.argv[1])
except ValueError:
    stderr('interval must be an integer')
    exit(1)
if interval <= 0:
    stderr('interval should be > 0')
    exit(1)

if len(sys.argv) == 3:
    device_file = sys.argv[2]
else:
    # try to automatically look up the file
    dir_pat = '/sys/bus/w1/devices/28*'
    dir_glob = glob.glob(dir_pat)
    if len(dir_glob) != 1:
        stderr('found {} matching dirs for {}'.format(len(dir_glob), dir_pat))
        exit(1)
    device_file = dir_glob[0] + '/w1_slave'


try:
    stderr('starting thermometer')
    while True:
        with open(device_file, 'r') as f:
            line = f.readline().strip()
            if line[-3:] != 'YES':
                stderr('bad crc checksum; retrying in {}s'.format(retry))
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
    stderr('stopping thermometer')
