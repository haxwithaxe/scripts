#!/bin/bash

sudo echo i r root # just to get a sudo session jumpstarted

#find all the cifs/smbfs mounts so we can unmount them
cifsmounts=`grep cifs /etc/mtab | egrep -o ' /[[:alnum:][:punct:]]*' | sed 's/[ \t]*//g'`
for i in $cifsmounts ;do
	sudo umount -l $i
done

# suspend the computer
sudo pm-suspend

# be polite when the computer starts back up
echo 'Hello!!! :)'
