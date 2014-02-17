#!/bin/bash
# copyright (c) 2014 haxwithaxe
# License: GPLv3

# call from root crontab via @reboot

# Update the system clock on non-rtc system

UTC='-u'
LOGFILE="/dev/null"

# try to correct time and exit if failure
ntpdate pool.ntp.org >$LOGFILE 2>&1 || exit 0

# wait for things to propagate
sleep 5

# one more time for good measure
ntpdate pool.ntp.org >$LOGFILE 2>&1 || exit 0

# set the hardware clock to the corrected system time
hwclock -w $UTC >> $LOGFILE 2>&1 || exit 0

