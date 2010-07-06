#!/bin/bash
file=$1
lines=$2
sum=0
if [[ -z $lines ]]
then echo "must specify question numbers: '1 2 3 4'" && exit 1
fi
if [[ -z $file ]]
then echo "please specify file to parse" && exit 1
fi
for i in `cat $file`
	do
	ln=`echo $i | cut -d':' -f1`
	n=`echo $i | cut -d':' -f2`
	for a in $lines; do
		if (( $ln == $a ))
			then
				export sum=`echo $n+${sum} | bc`
		fi
		echo -n .
	done
done
echo .
echo $sum
exit 0
