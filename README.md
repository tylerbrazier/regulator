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

[0]: https://www.adafruit.com/products/268
[1]: https://www.adafruit.com/products/381
[2]: https://learn.adafruit.com/adafruits-raspberry-pi-lesson-11-ds18b20-temperature-sensing/overview
[3]: https://pypi.python.org/pypi/RPi.GPIO
