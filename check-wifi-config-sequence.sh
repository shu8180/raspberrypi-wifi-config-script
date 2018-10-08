#!/bin/bash

if [ "$EUID" -ne 0 ]; then
    echo "Must be root"
    exit
fi

sleep 3
PREV_IP=`ifconfig wlan0 | awk '/inet / {print $2}'`
if [ "$PREV_IP"  != "192.168.10.1" ]; then
    echo $PREV_IP > /home/pi/raspberrypi-wifi-config-script/previous-ip 
fi

SEQUENCE=`cat /home/pi/raspberrypi-wifi-config-script/wifi-config-sequence`

if [ "$SEQUENCE" -eq "1" ]; then
    echo 2 > /home/pi/raspberrypi-wifi-config-script/wifi-config-sequence
    /home/pi/raspberrypi-wifi-config-script/wifi-config.sh
elif [ "$SEQUENCE" -eq "2" ]; then
    echo 0 > /home/pi/raspberrypi-wifi-config-script/wifi-config-sequence
    /usr/bin/python /home/pi/raspberrypi-wifi-config-script/wifi-config-site/server.py &
else
    echo 0 > /home/pi/raspberrypi-wifi-config-script/wifi-config-sequence
fi
