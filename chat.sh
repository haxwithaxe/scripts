#!/bin/bash
# Copyright 2014 haxwithaxe
# license cc0 ... cause this is so original :P

# cause i'm not lazy
if (screen -ls | grep -q chat) ;then
	screen -U -AD -x chat
else
	screen -U -S chat irssi
fi
