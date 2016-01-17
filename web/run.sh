#!/bin/bash
set -eu
cd "$(dirname "$0")"

# sign up at https://plot.ly
plotly_user=somebody
plotly_api_key=your-secret-key

# log file to collect data from
log=../logs/temperature.out.txt

# where to keep the server logs
stdout=../logs/web.out.txt
stderr=../logs/web.err.txt

node index.js "$log" "$plotly_user" "$plotly_api_key" >>"$stdout" 2>>"$stderr"
