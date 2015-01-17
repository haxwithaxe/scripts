#!/bin/bash

set -e

# run this at the beginning of every x session
# xhost +si:localuser:$(whoami)
export DISPLAY=:0.0

_play_cmd=echo
_beep(){
	beep -f4800 -l500 && beep -f2000 -l200 && beep -f2700 -l500 && beep -f1800 -l300
}

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
_play=${_play:-_beep} # paplay}

main(){
	message="${message:-ALARM} $0 $_play $_sound "

	while true ;do $_play $_sound ;done &

	play_pid=$!

	$_xmessage $message

	if [ `ps a | grep -q $play_pid` ] ;then
		kill -9 $play_pid
	else
		killall `basename $0`
	fi
}

main || exit 0
