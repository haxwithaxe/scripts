#!/bin/bash
isoTitle=$1
dd if=/dev/sr0 | bzip2 -9 > $isoTitle.iso.bz2
aplay resources/feca.wav
