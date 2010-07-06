#!/bin/bash
asm="$1"
date="`date +%y%m%d-%H%M`"
log="" #kismet name format
logdir="/home/chris/kismet-log/marc" # set to $2 after dev is done
type=""
mv_log() {
	cp/var/log/kismet/*.csv $logdir/$1/
	cp /var/log/kismet/*.network $logdir/$1/
	cp /var/log/kismet/*.xml $logdir/$1/ ;
}

print_help() {
echo 'Usage:'
echo 'kismet-marc-log-bak.sh (n | s | e | w ) logdir'
echo ;
}

if [ -z $1 ] # test input for an asm value
	then
		print_help
		exit 0
fi

case $1 in 
	n)
	  mv_log "northbound/"
	;;
	s)
	  mv_log "southbound/"
	;;
	e)
	  mv_log "eastbound/"
	;;
	w)
	  mv_log "westbound/"
	;;
	*) 
	  print_help
	  exit 1

esac

echo "done"

exit 0

