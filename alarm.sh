#!/bin/bash

# run this at the beginning of every x session
# xhost +si:localuser:$(whoami)
export DISPLAY=:0.0

TEMP=`getopt -o xgp:s:m: -- "$@"`

eval set -- "$TEMP"

while true ;do
	case $1 in
		-x)
			_xmessage=xmessage
			shift
			;;
		-g)
			_xmessage=gxmessage
			shift
			;;
		-p)
			_play=$2
			shift 2
			inmsg=false
			;;
		-s)
			_sound=$2
			shift 2
			inmsg=false
			;;
		-m)
			inmsg=true
			message=$2
			shift 2
			;;
		-d)
			export DISPLAY=$2
			shift 2
			;;
		--)
			shift
			break
			;;
		*)
			if $inmsg ;then
				message="$message $1"
			fi
			shift
			;;
	esac
done

_xmessage=${_xmessage:-gxmessage}
_sound=${_sound:-/usr/share/sounds/KDE-Sys-App-Error-Critical.ogg}
_play=${_play:-paplay}

message=${message:-"ALARM"}

while true ;do $_play $_sound ;done &

play_pid=$!

$_xmessage $message
kill -9 $play_pid
