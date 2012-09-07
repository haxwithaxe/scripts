#!/bin/bash

echo 'Time me please!!'

count=10
formatter="/usr/AHFormatterV52_64/run.sh"
fofile="test.fo"
outfile="/tmp/out.pdf"

while [ $count -ge 0 ];do

	$formatter -d $fofile -o $outfile

	count=$[$count-1]

done
