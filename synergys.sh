#!/bin/bash
# A mechanism to pass arbitrary condiments
#  and launch synergys with different configs
# Copyright haxwithaxe 2015
# License: GPLv3

set -e

synergys=/usr/bin/synergys
config_dir=$HOME/.config/synergy
default_profile=$config_dir/default.conf

if ! [ -d $config_dir ] ;then
	mkdir -p $config_dir
fi	

usage(){
	cat - >&2 <<EOM
$(basename $0) [-p|--profile <profile>] [-d|--default <profile>] [-c|--config <config file>] [-h|--help]
EOM

}

set_profile(){
	echo Creating profile: $profile
	mv $config $config_dir/${profile}.conf
}

set_default(){
	echo Set default profile to: $profile
	ln -sf $config_dir/${profile}.conf $default_profile
}

use_profile(){
	killall synergys || killall -9 synergys || true
	$synergys -c $config_dir/${profile}.conf
}

use_default(){
	killall synergys || killall -9 synergys || true
	$synergys -c $default_profile
}

list_profiles(){
	for p in `ls $config_dir/*.conf`;do
		echo $(basename $p .conf)
	done
}

validate_profile(){
	if [ ! -f "$config_dir/${profile}.conf" ]; then
		echo "ERROR: "${profile}" is not an existing profile." 1>&2
		usage
		exit 1
	fi
}

validate_default(){
	if [ "$default" != "default" ] && [ ! -f $config_dir/${default}.conf ] ;then
		echo -e "ERROR: The default profile is not set.\nuse: $(basename $0) --default <existing profile name> or $(basename $0) --default --config <config file>" >&2
		usage
		exit 1
	fi
}

validate_config(){
	if ! [ -f $config ]; then
		echo "ERROR: \"${config}\" is not a file." >&2
		usage
		exit 1
	fi
}

while getopts ":-:p:d:c:lh" opt;do
	case "$opt" in
		-)
			case "$OPTARG" in
				profile)
					profile="${!OPTIND}"
					OPTIND=$(( $OPTIND + 1 )) 
					validate_profile
					;;
				default)
					default="${!OPTIND}"
					case "$default" in
						--config)
							default=default
							;;
						-c)
							default=default
							;;
						*)
							OPTIND=$(( $OPTIND + 1 ))
							;;
					esac
					validate_default
					;;
				config)
					config="${!OPTIND}"
					OPTIND=$(( $OPTIND + 1 ))
					validate_config
					;;
				help)
					usage
					exit 1
					;;
				*)
					echo -n
					;;
			esac
			;;
		p)
			profile=$OPTARG
			validate_profile
			;;
		d)
			default=$OPTARG
			validate_default
            ;;
		c)
			config=$OPTARG
			validate_config
            ;;
		l)
			list_profiles
			exit 0
			;;
		h)
			usage
			exit 1
            ;;
		*)
			echo -n
			;;
	esac
done

if [ "$default" = "default" ] && [ -n "$config" ] ;then
	profile=$default
	set_profile
elif [ -n "$default" ] ;then
	profile=$default
	set_default
elif [ -n "$profile" ] && [ -n "$config" ] ;then
	set_profile
elif [ -n "$profile" ] ;then
	use_profile
elif [ -n "$config" ] ;then
	profile=tmp
	set_profile
	use_profile
	sleep 5
	rm $config_dir/tmp.conf
else
	use_default
fi

