#!/usr/bin/python

import GeoIP

gi = GeoIP.open("GeoLiteCity.dat",GeoIP.GEOIP_STANDARD)

def print_addr(ipaddr):
    gia = gi.record_by_addr(ipaddr)
    print gia['country_name']
    print gia['region']
    print gia['region_name']
    print gia['city']
    print gia['postal_code']

def print_name(dname):
   gin = gi.record_by_name(dname)
   print gin['country_name']
   print gin['region']
   print gin['region_name']
   print gin['city']
   print gin['postal_code']

print_name("www.google.com")
print
print_addr("64.233.161.104")

exit()