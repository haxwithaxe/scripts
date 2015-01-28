#!/usr/bin/env python2
''' Uses pywapi to grab the NOAA weather data. Uses google to translate zipcodes and addresses into gps coords and finds the nearest station.
Returns a string formatted for conky.

'''
__authors__ = ['haxwithaxe me@haxwithaxe.net']

__license__ = 'GPLv3'

import csv

station_headers = ('ind', 'pl', 'stabv', 'co', 'wmoreg', 'lat', 'lon', 'ualat', 'ualon', 'elev', 'uaelev', 'rbsn')

zip_headers = ("zip", "stabv", "lat", "lon", "city", "st")


class StationsDB:
    def __init__(self, stations_filename, zipcodes_filename):
        # stations => {'id':entry}
        self.stations = csv.DictReader(stations_filename, station_headers)
        self.zipcodes = csv.DictReader(zipcodes_filename, zip_headers)

    def zips_for_stations(self):
        """ Iterate over zipcodes and attach them to satations """
        pass

    def zip_to_station(self, zip):
        """ Find the station closest to the zipcode """
        best_dist, best_sta = 99999999,''
        for sta in self.stations:
            test_point = map(float, (sta['lat'], sta['lon']))
            distance = ((tlat-zip['lat'])**2 + (tlon-zip['lon'])**2)**0.5
            if distance < best:
                best_dist, best_sta = distance, sta
        return best_sta

    def zip_for_station(self, zip):
        """ Attach the zipcode to the station closest to it. """
        self.stations[zip_to_station(zip)]['zipcodes'].append(zip)

