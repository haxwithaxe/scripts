#!/bin/bash

sink=`pacmd info|grep "Default sink name"|awk '{print $4}'`
pacmd set-sink-mute $sink yes
