#!/bin/bash

sudo cat ./sources.list > /etc/apt/sources.list


sudo wget 'http://deb.playonlinux.com/playonlinux_jaunty.list' -O /etc/apt/sources.list.d/playonlinux.list

wget -q 'http://packages.medibuntu.org/medibuntu-key.gpg' -O- | sudo apt-key add - 

wget -q 'http://keyserver.ubuntu.com:11371/pks/lookup?op=get&search=0xA30749C0AA7D4E90' -O- | sudo apt-key add -

wget -q 'http://download.virtualbox.org/virtualbox/debian/sun_vbox.asc' -O- | sudo apt-key add -

wget -q 'http://wine.budgetdedicated.com/apt/Scott%20Ritchie.gpg' -O- | sudo apt-key add -

sudo apt-get update && sudo apt-get install non-free-codecs gstreamer0.10-plugins-base gstreamer0.10-plugins-good gstreamer0.10-plugins-ugly gstreamer0.10-plugins-base-multiverse gstreamer0.10-plugins-good-multiverse gstreamer0.10-plugins-bad gstreamer0.10-plugins-ugly-multiverse gstreamer0.10-plugins-bad-multiverse virtualbox-3.0 wine wine-gecko playonlinux libxine1-all-plugins totem-xine  p7zip-full unrar rar flashplugin-installer ubuntu-restricted-extras swfdec-gnome ttf-mscorefonts-installer sun-java6-plugin sun-java6-jre sun-java6-bin sun-java5-plugin sun-java5-jre sun-java5-bin unzip zip build-essential

exit 0
