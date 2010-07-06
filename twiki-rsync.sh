#!/bin/bash
## NOTES ##########################
## !!BE SURE TO ADD YOUR SSH KEY TO THE SERVER!!
## $0 Lives anywhere and is called by crontab preferably
## The variables at the top of the script must be changed
#  to reflect the appropriate values for you system
###################################
# $volume = the truecrypt volume
volume='/mega/arch/work/twiki'

# $mountdir = the place to mount the truecrypt volume
mountdir='/mnt/twiki'

# $keyfile = the key file used to unlock the truecrypt volume
keyfile='/mega/arch/work/twiki.jpg'

# $twikidir = the place where twiki lives on the server
twikidir='/usr/local/apache/htdocs/twiki'

## make sure $mountdir exists and if not try to create it
if ! [ -e $mountdir ];then
	echo "WARN: $mountdir DOES NOT EXIST!"
	echo "INFO: attempting to make $mountdir"
	if ( mkdir $mountdir ); then
		echo "INFO: $mountdir created successfully"
	else
		echo "ERROR: FAILED TO CREATE $mountdir"
		echo "INFO: please create $mountdir manually"
		exit 1
	fi
fi

## mount $volume on $mountdir without user input using $keyfile to
#  unlock the truecrypt volume
truecrypt $volume $mountdir --non-interactive -k $keyfile
wait

## drop into the encrypted volume and copy the new and updated files
#  from twikiserver to here
echo "INFO: moving to $mountdir"
cd $mountdir
echo "INFO: using rsync to copy twiki to $mountdir"
rsync -e 'ssh -ax -p7101' -avz twiki@tanuj.is-very-evil.org:${twikidir} .
wait

## go home and dismount the truecrypt volume
echo "INFO: going home"
cd ~
echo "INFO: unmounting $volume from $mountdir"
truecrypt --dismount $volume

## make sure everything is done and exit
wait
exit 0
