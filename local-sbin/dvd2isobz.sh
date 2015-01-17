#!/bin/bash
# turn a CD into an iso then bzip it.
isoTitle=$1
dd if=/dev/sr0 | bzip2 -9 > $isoTitle.iso.bz2
# play an annoying sound when done
aplay resources/feca.wav
