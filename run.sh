#!/bin/bash

interval=30

# for fermenting ale
#lower_bound=20
#upper_bound=22

# for keeping it cold
lower_bound=2
upper_bound=3

#rm -f stderr.log stdout.log

python3 thermometer.py $interval 2>>stderr.log | \
  sudo python3 regulator.py $lower_bound $upper_bound 2>>stderr.log >>stdout.log
