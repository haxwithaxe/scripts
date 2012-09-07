#!/bin/bash

CJDNS_IP="`/sbin/ifconfig -a | grep 'inet6 addr'|cut -d: -f2-|cut -d\  -f2|cut -d\/ -f1|grep ^fc`"
NICK="`echo $CJDNS_IP|cut -d: -f1`"

irssi \
--connect fcec:0cbd:3c03:1a2a:063f:c917:b1db:1695 \
-n $NICK \
--hostname=$CJDNS_IP


