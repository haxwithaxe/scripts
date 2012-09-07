#!/bin/bash

builddir="/root/multilib"
version="current"
ftpurl="http://slackware.com/~alien/multilib/"
ftpcmd="lftp -c open ${ftpurl} ; mirror ${version}"
cwd=`pwd`


cd $builddir && \

lftp -c 'open http://slackware.com/~alien/multilib/ ; mirror current' && \

cd current && \

upgradepkg --reinstall --install-new *.t?z && \

upgradepkg --install-new slackware64-compat32/*-compat32/*.t?z && \

echo -e '\n\nSuccessfully updated multilib libraries for Slackware64-current! :D'

cd $cwd
