#!/bin/sh

MOD_VALS=false
STRING_FORMAT="8s"

get_id_map(){
	gim_wids=( $(xprop -root | grep '_NET_CLIENT_LIST.*(WINDOW)' | sed 's/^.*#//' | sed 's/,/\n/g' | sort -u ) )
	for gim_wid in ${gim_wids[@]}; do
		gim_pid=`xprop -id $gim_wid 2>/dev/null | grep -P '_NET_WM_PID' | sed 's/[[:space:]]\+//g' | cut -d'=' -f2`
		if [ ! -z "$gim_pid" ] ;then
			echo $gim_pid,$gim_wid
		fi
	done
}

get_wids_for_pid(){
	gwfp_spid=$1
	gwfp_wids=${@:2}
	for gwfp_i in $gwfp_wids ;do
		gwfp_pid=${gwfp_i//,*/}
		gwfp_wid=${gwfp_i//*,/}
		if [ "${gwfp_pid}" -eq "${gwfp_spid}" ] ;then
			echo $gwfp_wid
		fi
	done
}

set_xprop(){
	sx_wid=$1
	sx_prop=$2
	sx_value=$3
	sx_format=$4
	echo "xprop -id $sx_wid $sx_format -set $sx_prop $sx_value"
    xprop -id $sx_wid $sx_format -set $sx_prop "$sx_value"
	return $?
}

mod_value(){
	mv_value=$1
	mv_wid=$2
	enabled=$3
	if $enabled ;then
	#	echo "${mv_value}-${mv_wid}" 1>&2
		echo "${mv_value}-${mv_wid}"
	else
    #    echo "$mv_value" 1>&2
		echo $mv_value
	fi
}

set_xprop_for_pid(){
	sxfp_pid=$1
    sxfp_prop=$2
    sxfp_value=$3
	sxfp_format="-f $sxfp_prop $4"
	sxfp_id_map=`get_id_map`
	sxfp_wids_for_pid=`get_wids_for_pid $sxfp_pid $sxfp_id_map`
	for sxfp_wid in $sxfp_wids_for_pid ;do
		#echo "set_xprop \"$sxfp_wid\" \"$sxfp_prop\" \"`mod_value $sxfp_value $sxfp_wid false`\" \"$sxfp_format\""
		set_xprop "$sxfp_wid" "$sxfp_prop" "`mod_value $sxfp_value $sxfp_wid false`" "$sxfp_format"
	done
}

set_class_for_pid(){
	class=$1
	pid=$2
	set_xprop_for_pid $pid "WM_CLASS" $class $STRING_FORMAT
}
