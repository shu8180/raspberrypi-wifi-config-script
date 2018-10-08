#!/bin/bash

if [ "$EUID" -ne 0 ]
	then echo "Must be root"
	exit
fi

sudo service hostapd stop
sudo service dnsmasq stop

sleep 2

systemctl disable hostapd
systemctl disable dnsmasq

cp /etc/network/interfaces.bak /etc/network/interfaces
cp /etc/dhcpcd.conf.bak /etc/dhcpcd.conf

sleep 2

sudo reboot
