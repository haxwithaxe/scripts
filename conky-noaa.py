#!/usr/bin/env python2
''' Uses pywapi to grab the NOAA weather data. Uses google to translate zipcodes and addresses into gps coords and finds the nearest station.
Returns a string formatted for conky.

'''
__authors__ = ['haxwithaxe me@haxwithaxe.net']

__license__ = 'GPLv3'

import pywapi
import urllib2
import json
from Weather.data import rows #FIXME replace with seperate db
import argparse

'''{   'dewpoint_c': u'-3.3',
    'dewpoint_f': u'26.1',
    'dewpoint_string': u'26.1 F (-3.3 C)',
    'icon_url_base': u'http://forecast.weather.gov/images/wtf/small/',
    'icon_url_name': u'sct.png',
    'latitude': u'40.66',
    'location': u'New York/John F. Kennedy Intl Airport, NY',
    'longitude': u'-73.78',
    'ob_url': u'http://www.weather.gov/data/METAR/KJFK.1.txt',
    'observation_time': u'Last Updated on Mar 27 2013, 10:51 am EDT',
    'observation_time_rfc822': u'Wed, 27 Mar 2013 10:51:00 -0400',
    'pressure_in': u'29.92',
    'pressure_mb': u'1013.2',
    'pressure_string': u'1013.2 mb',
    'relative_humidity': u'44',
    'station_id': u'KJFK',
    'suggested_pickup': u'15 minutes after the hour',
    'suggested_pickup_period': u'60',
    'temp_c': u'8.3',
    'temp_f': u'47.0',
    'temperature_string': u'47.0 F (8.3 C)',
    'two_day_history_url': u'http://www.weather.gov/data/obhistory/KJFK.html',
    'weather': u'Partly Cloudy',
    'wind_degrees': u'310',
    'wind_dir': u'Northwest',
    'wind_gust_mph': u'20.7',
    'wind_mph': u'13.8',
    'wind_string': u'from the Northwest at 13.8 gusting to 20.7 MPH (12 gusting to 18 KT)',
    'windchill_c': u'5',
    'windchill_f': u'41',
    'windchill_string': u'41 F (5 C)'}'''

def address2station(loc):
    '''
    Translate full location into Station tuple by closest match
    Locations can be in any Google friendly form like
    "State St, Troy, NY", "2nd st & State St, Troy, NY" and "7 State St, Troy, NY"
    '''
    location = str(loc).replace(' ','+')
    geo_url = 'http://maps.googleapis.com/maps/api/geocode/json?sensor=false&address=%s'%location
    req = urllib2.urlopen(geo_url)
    result = json.loads(req.read())
    point = map(float,[result['results'][0]['geometry']['location']['lat'], result['results'][0]['geometry']['location']['lng']])
    best,close = 99999999,[]
    for row in rows():
        test_point = map(float, (row[2],row[3]))
        distance = ((test_point[0]-point[0])**2 + (test_point[1]-point[1])**2)**.5
        if distance < best:
            best,close = distance,row
    return close[0]


parser = argparse.ArgumentParser()
parser.add_argument('-s', '--station', dest='station', required=False)
parser.add_argument('-l', '--location', dest='location', required=False)
args = parser.parse_args()

station = args.station

try:
    if args.location:
        station = address2station(args.location)

    noaa_result = pywapi.get_weather_from_noaa(station)

    print(' '.join(['cur:%s' % (noaa_result.get('weather') or ''), 
            '%sC' % (noaa_result.get('temp_c') or '?'), 
            'chill:%sC' % (noaa_result.get('windchill_c') or '?'), 
            'hu:%s%%' % (noaa_result.get('relative_humidity') or '?')]))
except:
    print('weather error')
