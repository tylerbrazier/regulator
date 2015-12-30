Regulator
=========
Monitor and regulate freezer temperature with raspberry pi

You can get all of the hardware for this project from Adafruit and they have
a really nice [guide][0] for using the temperature sensor.

Run `setup.sh` as root to configure kernel modules and reboot.

The `thermometer.py` script prints temperature readings at regular intervals.
E.g. every 5 seconds: `python3 thermometer.py 5`.

[0]: https://learn.adafruit.com/adafruits-raspberry-pi-lesson-11-ds18b20-temperature-sensing/overview
