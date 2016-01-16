#!/bin/bash
set -eu
cd "$(dirname "$0")"

# how often (in seconds) to take temp readings
interval=60

# when temp (in Celsius) falls below this number, turn off the freezer
lower_bound=4

# when temp exceeds this number, turn the freezer on
upper_bound=8

# where to put the logs
stdout=../logs/temperature.out
stderr=../logs/temperature.err

python3 thermometer.py "$interval" 2>>"$stderr" | \
  sudo python3 regulator.py "$lower_bound" "$upper_bound" 2>>"$stderr" >>"$stdout"
