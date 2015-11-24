#!/bin/bash

primary=eDP1
secondary=$(xrandr | grep ' connected' | grep -v $primary | cut -d' ' -f1)
while [[ "$secondary" == "" ]]; do
	sleep 1
	secondary=$(xrandr | grep ' connected' | grep -v $primary | cut -d' ' -f1)
done
echo secondary display is: $secondary
xrandr --output $secondary --auto
xrandr --output $secondary --right-of $primary
