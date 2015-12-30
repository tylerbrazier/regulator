#!/bin/bash
set -eu

# configure w1-gpio module to use pin 4 by default. for more info:
# https://github.com/raspberrypi/firmware/blob/master/boot/overlays/README
bootfile="/boot/config.txt"
line="dtoverlay=w1-gpio"
! grep -q "^$line" "$bootfile" && echo "$line" >> "$bootfile"


# configure linux to load w1 modules on boot.
# modules-load.d is the modules directory on Arch, raspbian might be different
modfile="/etc/modules-load.d/w1.conf"
[ ! -f "$modfile" ] && echo '
w1-gpio
w1-therm
' > "$modfile"


echo "Remember to reboot!"
