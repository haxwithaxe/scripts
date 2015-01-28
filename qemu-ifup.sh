#!/bin/bash

export PATH=/root/.bin:/usr/local/sbin:/usr/local/bin:/sbin:/usr/sbin:/bin:/usr/bin:/sbin:/usr/sbin:/usr/local/sbin

switch=br0

set -e

if [ -n "$1" ] ;then
	sudo tunctl -u `whoami` -t $1
	sudo ip link set $1 up
	sleep 2
	sudo brctl assif $switch $1
	exit 0
else
	echo "Error: No interface specified"
	exit 1
fi
