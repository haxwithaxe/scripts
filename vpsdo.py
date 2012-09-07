#!/usr/bin/env python3

import sys
import re
import getopt
import http.client
import urllib.parse

success = {'status':{'status':'success','statusmsg':('offline','online'),'vmstat':'online','fix':{'online':None,'offline':None}},
'reboot':{'status':'success','statusmsg':'rebooted','vmstat':'online','fix':{'online':'reboot','offline':'boot'}},
'boot':{'status':'success','statusmsg':'booted','vmstat':'online','fix':{'offline':'boot'}},
'shutdown':{'status':'success','statusmsg':'shutdown','vmstat':'offline','fix':{'online':'shutdown'}}}

usage = 'useage: '+sys.argv[0]+' -a <status|reboot|boot|shutdown> ( -f <api auth file> | -k <api key> -x <api hash> ) [--help|-h]\n'

def processresponse(data):
	output = {}
	data = str(data).replace('b','',1).strip('\'')
	for i in re.findall('<[^>/]*>[^<]*',data):
		item = i.strip('<').split('>')
		output[item[0].strip()] = item[1].strip()
	return output

def callSolusVMAPI(action,apikey,apihash):
	params = urllib.parse.urlencode({'key':apikey,'hash':apihash,'action':action,'status':'true'})
	headers = {'Content-Type':'application/x-www-form-urlencoded','Accept':'text/plain'}
	conn = http.client.HTTPSConnection('cp.thrustvps.com')
	conn.request('POST','/api/client/command.php',params,headers)
	response = conn.getresponse()
	print(response.status, response.reason)
	if response.status != 200:
		if response.status == 0: response.status = 1
		sys.exit(response.status)
	data = response.read()
	conn.close()
	return processresponse(data)

def getapibits(config=False):
	global apikey
	global apihash
	global apifile
	if False in (apikey,apihash) and apifile:
		fileobj = open(apifile,'r')
		apikey, apihash = [ x.strip() for x in fileobj.read().strip().split('\n') ]
		fileobj.close()
	else:
		sys.exit(491)
	return apikey, apihash

def main(action):
	if not action: sys.exit(0)
	apikey, apihash = getapibits()
	status = callSolusVMAPI(action,apikey,apihash)
	if status['status'] == 'success':
		print(action+' completed successfully')
	if status['statusmsg'] not in success[action]['statusmsg']:
		print('action: '+action+' failed\nstatus: '+status['statusmsg']+'\nvps is '+status['vmstat']+' trying to fix')
		main(success[action]['fix'][status['vmstat']])

if __name__ == '__main__':
	global apikey
	global apihash
	global apifile
	action  = apikey = apihash = apifile = missedarg = False
	opts, args = getopt.gnu_getopt(sys.argv[1:], 'k:x:a:f:h', ['help'])
	opts = dict(opts)
	if '-h' in opts or '--help' in opts:
		print(usage)
		sys.exit(0)
	if '-k' in opts: apikey = opts['-k']
	if '-x' in opts: apihash = opts['-x']
	if '-a' in opts: action = opts['-a']
	if '-f' in opts: apifile = opts['-f']
	if not action:
		print('-a or --action is required')
		missedarg = True
	if not apifile and False in (apikey,apihash):
		print('either -k and -x, or -f are required')
		missedarg = True
	if missedarg: sys.exit(1)
	main(action)
	
