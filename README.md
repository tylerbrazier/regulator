Regulator
=========
Monitor and regulate freezer temperature with raspberry pi. I started this
project because my chest freezer's highest temperature setting is still too cold
to keep my homebrew chilled. The goal is to be able to monitor temperature with
pi and have the freezer's power hooked up to a relay that can be switched off
when the temperature gets too cold.

I got most of my hardware from Adafruit, including the [relay][0] and
[temperature sensor][1]. They also have a really nice [guide][2] that I
followed for using the temperature sensor.

Run `setup.sh` as root to configure kernel modules and reboot.

The `thermometer.py` script can be used independently and prints temperature
readings at regular intervals. E.g. every 30 seconds:

    python3 thermometer.py 30

To control the relay based on the temperature, pipe the output of
`thermometer.py` to `regulator.py`. See `run.sh`. Note that the regulator
script requires [RPi.GPIO][3].

Web
---
The project also includes a little web server that can be queried for logs
and their statistics for any given period of time. Plots can also be generated
using [plot.ly][4].

Start the server on port 8080:

    node web/index.js logs/stdout.log PLOTLY_USER  PLOTLY_API_KEY

To see stats for the last 2 hours with a plot: `/stats?period=2h&plot=true`.
Period measures are: `m = minutes, h = hours, d = days, w = weeks`.
If no period is given, the default is `1d`.

Logs are at `/logs`.

[0]: https://www.adafruit.com/products/268
[1]: https://www.adafruit.com/products/381
[2]: https://learn.adafruit.com/adafruits-raspberry-pi-lesson-11-ds18b20-temperature-sensing/overview
[3]: https://pypi.python.org/pypi/RPi.GPIO
[4]: https://plot.ly
