#!/bin/bash

# die hard
set -e

# where synergyc will look for a server
SYNERGYS_IP=${SYNERGYS_IP:-yoshi} #yoshi == server

# force synergyc to use :0.0 rather than the lack of X display in an 
#  ssh session or the forwarded display
# also pass any extra args and then the server ip
synergyc --display :0.0 $@ $SYNERGYS_IP
