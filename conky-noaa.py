#!/usr/bin/env python2

''' Uses pywapi to grab the NOAA weather data. Uses google to translate zipcodes and addresses into gps coords and finds the nearest station.
Returns a string formatted for conky. '''

__authors__ = ['haxwithaxe me@haxwithaxe.net']
__license__ = 'GPLv3'

import sys
import pywapi
import urllib2
import json
import csv
import argparse


''' noaa-conky:
    print a formatted string for consumption by i3bar via conky containing weather data from NOAA based on either the zipcode or the station ID.
    Usage:
        noaa-conky.py [-s|--station <station ID>] [-l|--location <zipcode> --stationdb <stations.csv> --zipcodedb <zipcodes.csv>]

    example NOAA weather data:
    { 'dewpoint_c': u'-3.3',
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


def get_cvs_dict(filename, keys):
    csvfile = open('station-locations.csv', 'r')
    csv_lines = csv_file.readlines()
    csv_file.close()
    return csv.DictReader(csv_lines, keys)


def address2station(loc, stas, zips):
    """ Translate full location into Station tuple by closest match
        Locations can be in any Google friendly form like
        "State St, Troy, NY", "2nd st & State St, Troy, NY" and "7 State St, Troy, NY" """
    location = str(loc).replace(' ','+')
    geo_url = 'http://maps.googleapis.com/maps/api/geocode/json?sensor=false&address=%s'%location
    req = urllib2.urlopen(geo_url)
    result = json.loads(req.read())
    result_loc = result['results'][0]['geometry']['location']
    zlat, zlon = map(float,[results_loc['lat'], result['lng']])
    best_dist, best_sta = 99999999, None
    for sta in get_csv_dict(stas):
        stalat, stalon = map(float, (sta['lat'], sta['lon']))
        distance = ((stalat-zlat)**2 + (stalon-zlon)**2)**0.5
        if distance < best_dist:
            best, best_sta = distance, sta
    return best_sta


def handle_args(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', dest='station', default=None, required=False)
    parser.add_argument('-l', dest='location', default=None, required=False)
    parser.add_argument('-i', dest='stationdb', default=None, required=False)
    parser.add_argument('-j', dest='zipcodedb', default=None, required=False)
    args = parser.parse_args()
    return args


def get_weather_data(station=None, location=None, stations=None, zipcodes=None):
    try:
        if location and not station:
            station = address2station(location, stations, zipcodes)
        noaa_result = pywapi.get_weather_from_noaa(station)
        return noaa_result
    except:
        print('weather error')
        sys.exit(0)


def make_message(noaa_result):
    wmsg = []
    if noaa_result.get('weather'):
        wmsg.append('cur:%s' % noaa_result.get('weather'))
    if noaa_result.get('temp_c'):
        wmsg.append('%sC' % noaa_result.get('temp_c'))
    if noaa_result.get('windchill_c'):
        wmsg.append('chill:%sC' % noaa_result.get('windchill_c'))
    if noaa_result.get('relative_humidity'):
        wmsg.append('hu:%s%%' % noaa_result.get('relative_humidity'))
    if len(wmsg) < 1:
        return 'weather error'
    return ' '.join(wmsg)


if __name__ == '__main__':
    args = handle_args(sys.argv)
    # get weather data from NOAA based on zipcode, address, or station ID
    wdata = get_weather_data(args.station, args.location, args.stationdb, args.zipcodedb)
    wmsg = make_message(wdata)
    print(wmsg)
