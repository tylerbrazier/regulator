#!/bin/bash
set -eu
cd "$(dirname "$0")"

interval=60
lower_bound=2
upper_bound=3
out=logs/stdout.log
err=logs/stderr.log

rm -rf logs
mkdir -p logs

python3 thermometer.py $interval 2>>$err | \
  sudo python3 regulator.py $lower_bound $upper_bound 2>>$err >>$out
