Regulator
=========
Monitor and regulate freezer temperature with raspberry pi. I started this
project because my chest freezer's highest temperature setting is still too cold
to keep my homebrew chilled, so I want to regulate the power with a relay.

There's also a little web server for serving up logs and their statistics for
any given period of time. Plots can also be generated using [plot.ly][0].

Setup
-----
I got most of the hardware from Adafruit, including the [relay][1] and
[temperature sensor][2]. They also have a really nice [guide][3] that I
followed for using the sensor.

I'm running [Arch linux][4] on my pi so I haven't tested any of this with
Raspbian or other distros.

Install nodejs, python 3, and [RPi.GPIO][5]. Run `setup.sh` as root to
configure kernel modules and install web dependencies. Then reboot the pi.

Usage
-----
Modify `controls/run.sh` as needed and execute it to start the thermometer and
regulator. Similarly, edit and run `web/run.sh` to start the web server.

To see stats for the last 2 hours with a plot, browse to

    http://<pi's IP>:8080/stats?period=2h&plot=true

Period measures are: `m = minutes, h = hours, d = days, w = weeks`.
If no period is given, the default is `1d`.

Logs are at `http://<pi's IP>:8080/logs`.

Service files
-------------
The project also includes systemd service files for daemonizing the regulator
and web server. Edit them as needed, then as root:

    cp systemd/* /etc/systemd/system/

    # start them:
    systemctl start regulator-controls
    systemctl start regulator-web

    # make sure they're working:
    systemctl status regulator-controls
    systemctl status regulator-web

    # to have them start at boot:
    systemctl enable regulator-controls
    systemctl enable regulator-web

[0]: https://plot.ly
[1]: https://www.adafruit.com/products/268
[2]: https://www.adafruit.com/products/381
[3]: https://learn.adafruit.com/adafruits-raspberry-pi-lesson-11-ds18b20-temperature-sensing/overview
[4]: http://archlinuxarm.org/platforms/armv6/raspberry-pi
[5]: https://pypi.python.org/pypi/RPi.GPIO
