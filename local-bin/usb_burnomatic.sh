#!/bin/bash

if [ $UID -ne 0 ] ;then
	echo "Must be root to execute!"
	exit 1
fi

exclude="/dev/sda" # case regex syntax

known_good_md5="d58bc15213a3c7440974e7b5d46f8812"

ISO="/home/hax/known_good_usb.img"

md5_only(){
	drive=$1
	md5=$2
	drive_md5=`md5sum $drive | cut -d' ' -f1`
	echo Known good ${md5}
	echo $drive $drive_md5
	if [ "$drive_md5" = "${md5}" ] ;then
		echo Hash matches
		return 0
	else
		echo "ERROR: Drive $drive failed checksum" 1>&2
		return 1
	fi
}

burn_usb_from_hybrid_iso(){
	iso=$1
	drive=$2
	md5=$3
	dd if=$iso of=$drive
	ret=$?
	if [ $ret -eq 0 ] ;then
		sync
		drive_md5=`md5sum $drive | cut -d' ' -f1`
		echo Known good ${md5}
		echo $drive $drive_md5
		if [ "$drive_md5" = "${md5}" ] ;then
			echo Successfully burned drive $drive
			return 0
		else
			echo "ERROR: Drive $drive failed checksum" 1>&2
		fi
	else
		echo "ERROR: Failed to burn drive $drive" 1>&2
		return 1
	fi
}

for i in /dev/sd? ;do 
	case "$i" in
		"$exclude")
			echo Skipping drive $i
			;;
		*)
			echo Burning to drive $i
			if [ "$1" = "-md5" ] ;then 
				md5_only "$i" "$known_good_md5" &
			else
				burn_usb_from_hybrid_iso "$ISO" "$i" "$known_good_md5" &
			fi
			;;
	esac
done

wait
echo !!! Done !!!
aplay /usr/share/sounds/pop.wav
