#!/bin/bash

# Caps lock = Mod4 (used by xmonad)
xmodmap -e "clear lock" # drop Caps_Lock
xmodmap -e "remove mod4 = Hyper_L" # remove redundant Hyper_L references
xmodmap -e "keycode 66 = Hyper_L" # set Caps_Lock key to read as Hyper_L
xmodmap -e "add mod3 = Hyper_L" # set  mod3 to be Hyper_L
xmodmap -pm
