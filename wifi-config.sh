#!/bin/bash

if [ "$EUID" -ne 0 ]
	then echo "Must be root"
	exit
fi

cp /etc/network/interfaces /etc/network/interfaces.bak

sed -i -- 's/iface wlan0 inet manual//g' /etc/network/interfaces
sed -i -- 's/    wpa-conf \/etc\/wpa_supplicant\/wpa_supplicant.conf//g' /etc/network/interfaces
sed -i -- 's/#DAEMON_CONF=""/DAEMON_CONF="\/etc\/hostapd\/hostapd.conf"/g' /etc/default/hostapd

cat >> /etc/network/interfaces <<EOF
allow-hotplug wlan0
iface wlan0 inet static
	address 192.168.10.1
	netmask 255.255.255.0
	network 192.168.10.0
	broadcast 192.168.10.255
EOF

cp /etc/dhcpcd.conf /etc/dhcpcd.conf.bak

echo "denyinterfaces wlan0" >> /etc/dhcpcd.conf

systemctl enable hostapd
systemctl enable dnsmasq

sudo service hostapd start
sudo service dnsmasq start

sleep 2

sudo reboot
