#!/usr/bin/env python

'''convert meters to degrees lat'''

import math
import sys

EQUITORIAL_R = 6378137.0
POLAR_R = 6356752.3

class point:
	def __init__(self,x,y,z = 0):
		self.x = x
		self.y = y
		self.z = z

	def __init__(self):
		self.x = 0
		self.y = 0
		self.z = 0

	def in_rad(self,x,y,z=0):
		self.x = math.radians(x)
		self.y = math.radians(y)
		self.z = z

def _radius_at_lat(lat):
	divisor = (((EQUITORIAL_R**2) * math.cos(lat))**2)+(((POLAR_R**2) * math.sin(lat))**2)
	denominator = ((EQUITORIAL_R * math.cos(lat))**2)+((POLAR_R * math.sin(lat))**2)
	return math.sqrt(divisor/denominator)

'''Radius of the earth in meters: ():equitorial,(p1):at point,(p1,p2):avg between radius at p1 and radius at p2'''
def R(p1 = False,p2 = False):
	if not p1 and not p2: return EQUITORIAL_R
	elif not p2:
		return _radius_at_lat(p1.y)
	else:
		r1 = _radius_at_lat(p1.y)
		r2 = _radius_at_lat(p2.y)
		return (r1 + r2)/2
	
def pdelta(p1,p2): # Compute lengths of degrees
	return R() * (math.sin(p1.y) * math.sin(p2.y) + math.cos(p1.y) * math.cos(p2.y) * math.cos(p2.x - p1.x))

def m2deg_at_p(m,p):
	p1 = point()
	p1.in_rad(p.x+0.5,p.y+0.5)
	p2 = point()
	p2.in_rad(p.x-0.5,p.y-0.5)
	m_in_deg = pdelta(p1,p2)
	print(m,m_in_deg)
	return m/m_in_deg

if __name__ == '__main__':
	if not len(sys.argv) in [4]:
		print('usage: ...')
		sys.exit(1)
	if len(sys.argv) == 4:
		p = point()
		dist = float(sys.argv[1])
		p.in_rad(float(sys.argv[2])+0.5,float(sys.argv[3])+0.5)
		msg = 'Degrees latitude to meters at point '+sys.argv[2]+','+sys.argv[3]+': %d deg'

	print(msg % m2deg_at_p(dist,p))

