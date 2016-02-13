#!/bin/bash

set -e

update-grub

grep md0 /proc/mdstat | sed 's/\[[^ ]\+//g;s/ /\n/g' | grep 'sd*' | xargs -I'{}' grub-install /dev/{}
