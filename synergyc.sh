#!/bin/bash

# Launch synergy with some default options and some helpers
#
# Args:
#	-s: Synergy server hostname or IP.
#	-r: Restart synergyc if it is already running (for restarting with cron).
#	-v: Get verbose output.
#   -h: Show usage.
#	$@: All unused arguments are passed to synergyc.

SYNERGYC=/usr/bin/synergyc
CONFIG_DIR=$HOME/.config/synergy
CONFIG_FILE=$CONFIG_DIR/synergyc.conf
VERBOSE=false
CHECK_RUNNING=false
DO_RESTART=false

# run fast, die hard, and be easy to debug
set -e

verbose(){
	if $VERBOSE; then
		echo $@
	fi
}

usage(){
	echo "$(basename $0) [-s <server name/ip>] [-h] [<arguments for synergyc>] [-r] [-v]"
}

check(){
	pgrep '^synergyc$' >/dev/null 2>&1
}

_restart(){
	if check; then
		verbose "running"
		return 0
	else
		verbose "not running"
		return 1
	fi
}

synergy_args=''

while getopts "s:vhcr" opt; do
  case $opt in
	v)
		VERBOSE=true
		;;
    s)
    	SYNERGYS_IP=$OPTARG
    	;;
	c)
		CHECK_RUNNING=true
		;;
	r)
		DO_RESTART=true
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

if $CHECK_RUNNING; then
	set +e
	check
	exit $?
elif $DO_RESTART; then
	_restart
fi

# where synergyc will look for a server
if [ -z $SYNERGYS_IP ]; then
	SYNERGYS_IP=$(grep server_hostname $CONFIG_FILE 2>/dev/null | cut -d'=' -f2- )
	verbose "server_hostname is $SYNERGYS_IP"
	if [ -z $SYNERGYS_IP ]; then
		echo "Either specify a synergy server with -s or with server_hostname=<hostname> in $CONFIG_FILE."
		exit 1
	fi
fi

# kill remaining instances of synergyc so this doesn't conflict
killall synergyc 2>/dev/null || true

# force synergyc to use :0.0 rather than the lack of X display in an 
#  ssh session or the forwarded display
# also pass any extra args and then the server ip
synergyc_cmd="synergyc --display :0.0 $synergy_args $SYNERGYS_IP"
if $VERBOSE; then
	set -x
	$synergyc_cmd
else
	$synergyc_cmd >/dev/null 2>&1
fi
