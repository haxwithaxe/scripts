#!/bin/bash

# die hard
set -e

usage(){
	echo "$(basename $0) [-s <server name/ip>] [-h] [<arguments for synergyc>]"
}
synergy_args=''

while getopts "s:h" opt; do
  case $opt in
    s)
    	SYNERGYS_IP=$OPTARG
    	;;
    h)
    	usage
		exit 1
    	;;
	*)
		synergy_args="${synergy_args} $OPTARG"
		;;
  esac
done

# where synergyc will look for a server
SYNERGYS_IP=${SYNERGYS_IP:-lenny} #yoshi == server

# kill remaining instances of synergyc so this doesn't conflict
killall synergyc || true

# force synergyc to use :0.0 rather than the lack of X display in an 
#  ssh session or the forwarded display
# also pass any extra args and then the server ip
synergyc --display :0.0 $synergy_args $SYNERGYS_IP
