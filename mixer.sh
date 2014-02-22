#!/bin/bash
# Copyright (c) 2014 haxwithaxe
# License GPLv3

SYSTEM=alsa
INC=5

alsa_master_up(){
	amixer sset Master,0 ${INC}+
}
export alsa_master_up

alsa_all_up(){
	alsa_master_up
}
export alsa_all_up

alsa_master_down(){
	amixer sset Master,0 ${INC}-
}
export alsa_master_down

alsa_all_down(){
	alsa_master_down
}
export alsa_all_down

alsa_master_mute(){
    amixer sset Master,0 toggle
}

export alsa_master_mute

alsa_all_mute(){
	amixer sset Master,0 toggle
}
export alsa_all_mute

alsa_mic_up(){
    amixer sset Capture,0 ${INC}+
}
export alsa_mic_up

alsa_mic_down(){
	    amixer sset Capture,0 ${INC}-
}
export alsa_mic_down

alsa_mic_mute(){
    amixer sset Capture,0 toggle
}
export alsa_mic_mute

#pulse_master_up(){}

#pulse_master_down(){}

#pulse_all_mute(){}

set -x
${SYSTEM}_${1}_${2}
