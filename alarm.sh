#!/bin/bash

_sound=${HOME}/resources/sounds/REDALERT.wav
_play=paplay

message=${1:-"ALARM"}

while true ;do $_play $_sound ;done &

play_pid=$!

gxmessage $message
kill -9 $play_pid
