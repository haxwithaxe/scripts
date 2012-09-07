#!/usr/bin/env python

import math

dipolegain = 10 * math.log(1.64)/math.log(10)
Ax

def dbW2W(pdbW):
	return  (10**(pd/10)*100000)/100000

def W2dbW(pW):
	return (10 * math.log(pw)/math.log(10) * 100000)/100000

def getERP(Tx,Ax,tx_unit = 'W',ax_unit = 'dbi'):
	ERP_dbW = W2dbW(Tx_W) + Ax_dbi
	return dbW2W(ERP_dbW)


def _getTx_num(rcounter = 0):
	print('Enter transmitter power:')
	txp = raw_input().strip()
	if len(txp) < 1 or not txp.isdigit():
		print('''i'm dumb give it to me in straight int's or floats :P''')
		return _getTx_num(rcounter + 1)
	else:
		return float(txp)

def _getAx_num(rcounter = 0):
	print('Enter antenna gain:')
	ag = raw_input().strip()
	if len(ag) < 1 or not ag.isdigit():
		print('''i'm dumb give it to me in straight int's or floats :P''')
		return _getAx_num(rcounter + 1)
	else:
		return float(ag)

def _getTx_unit(rcounter = 0):
	print('Enter unit of tranmiter power (W/mW/dbW default:W):')
	txu = raw_input().strip()
	if len(txu) < 1 or txu not in TxUNITS:
		print('''that's not an option ... check your caps?''')
		return _getTx_unit(rcounter + 1)
	else:
		return txu

def _getAx_unit(rcounter = 0):
	print('Enter unit of antenna gain (dbW/dbi/W default:dbi):')
	axu = raw_input().strip()
	if len(axu) < 1 or axu not in AxUNITS:
		print('''that's not an option ... check your caps?''')
		return _getAx_unit(rcounter + 1)
	else:
		return axu



if __name__ == '__main__':
	print('Enter transmitter power:')
	txp = raw_input().strip()
	if len(txp) < 1:
	print('Enter unit of tranmiter power:')
	txpu = raw_input().strip()
	print('Enter antenna gain:')
	ag = raw_input()

