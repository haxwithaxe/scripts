#!/bin/bash

comments=$1
e1=Formatter
v1=6.0mr1
e2=Formatter
v2=6.0mr1e

if [[ $2 == 'write' ]] ;then
	write=true
fi

for i in `sed "s/ /;;;/g" ${comments}` ;do
	l=${i//;;;/ }
	c='<report-comment>'${l//\/*/}'<\/report-comment>\n<\/report>\n'
	p=${l//* /}/*-${e1}-${v1}_vs_${e2}-${v2}.xml
	if [ -z $write ] ;then
		sed "s/<\/report>/${c}/" $p
	else
		sed -i "s/<\/report>/${c}/" $p
	fi
done

