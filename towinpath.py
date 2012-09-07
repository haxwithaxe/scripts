#!/usr/bin/env python

import sys,re

drive = '\\'
drivetypes = {'net':{'start':'\\\\','end':'\\'}}

path = sys.argv[1]
if len(sys.argv) > 2:
	drive = sys.argv[2]
	if drive.split(':')[0] in drivetypes:
		dtype,drive = drive.split(':',1)
		drive = drivetypes[dtype]['start']+drive+drivetypes[dtype]['end']

print(drive+path.replace('\\','').replace('/','\\'))
