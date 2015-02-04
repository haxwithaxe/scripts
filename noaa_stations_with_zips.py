#!/usr/bin/env python2
""" Attach zipcodes that have a station closest to it to that station. """

__authors__ = ['haxwithaxe me@haxwithaxe.net']

__license__ = 'GPLv3'

import csv
import re
import logging as logger


class StationsDB(object):
    """ Stations database class. """

    def __init__(self, stations_filename, zipcodes_filename):
        """ Load stations and zipcodes.

        stations_filename   filename.
        zipcodes_filename   filename.
        """
        self.station_headers = ('stanum', 'blk', 'ind', 'pl', 'stabv', 'co',
                                'wmoreg', 'lat', 'lon', 'ualat', 'ualon',
                                'elev', 'uaelev', 'rbsn')
        self.zip_headers = ("zip", "stabv", "lat", "lon", "city", "st")
        self.stations = {}
        self._load_stations(stations_filename)
        self.zipcodes = []
        self._load_zipcodes(zipcodes_filename)

    def _load_stations(self, filename):
        # stations => {'id':entry}
        with open(filename, "rb") as csvfile:
            dialect = csv.Sniffer().sniff(csvfile.read(1024))
            csvfile.seek(0)
            stations_db = csv.DictReader(csvfile, fieldnames=self.station_headers, dialect=dialect)
            for station in stations_db:
                station.update({'lat':self._degmin_to_decdeg(station.get('lat')), 'lon': self._degmin_to_decdeg(station.get('lon')), "zipcodes":[]})
                self.stations.update({station.get('ind'): station})

    def _load_zipcodes(self, filename):
        with open(filename, "r") as csvfile:
            dialect = csv.Sniffer().sniff(csvfile.read(1024))
            csvfile.seek(0)
            zipcodes_db = csv.DictReader(csvfile, fieldnames=self.zip_headers, dialect=dialect)
            for zipcode in zipcodes_db:
                zipcode.update({"lat": float(zipcode.get("lat")), "lon": float(zipcode.get("lon"))})
                self.zipcodes.append(zipcode)


    def get_db(self):
        self.zips_for_stations()
        return self.stations

    def zips_for_stations(self):
        """ Iterate over zipcodes and attach them to satations """
        for zipcode in self.zipcodes:
            self.zip_for_station(zipcode)

    def zip_to_station(self, zipcode):
        """ Find the station closest to the zipcode """
        best_dist, best_sta = 99999999,''
        for sta_id, sta in self.stations.items():
            tlat, tlon = sta.get('lat'), sta.get('lon')
            distance = ((tlat-zipcode.get('lat'))**2 + (tlon-zipcode.get('lon'))**2)**0.5
            if distance < best_dist:
                best_dist, best_sta = distance, sta_id
        logger.debug("zipcode: %s, station:%s", zipcode.get("zip", "no zipcode"), best_sta)
        return best_sta

    def zip_for_station(self, zipcode):
        """ Attach the zipcode to the station closest to it. """
        station = self.zip_to_station(zipcode)
        self.stations[station]['zipcodes'].append(zipcode.get("zip"))

    def _degmin_to_decdeg(self, dm_str):
        """Return decimal representation of DMS """
        dms_str = re.sub(r'\s', '', dm_str)
        if re.match('[swSW]', dms_str):
            sign = -1
        else:
            sign = 1
        (degree, minute, junk) = re.split('\D+', dms_str, maxsplit=2)
        return sign * (int(degree) + float(minute) / 60 / 36000)


if __name__ == '__main__':
    import sys
    stations_filename = sys.argv[1]
    zipcodes_filename = sys.argv[2]
    output_filename = sys.argv[3]
    stations_db = StationsDB(stations_filename, zipcodes_filename)
    with open(output_filename, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=list(stations_db.station_headers)+['zipcodes'])
        writer.writeheader()
        for station in stations_db.get_db().values():
            #print(station)
            station["zipcodes"] = " ".join(station.get("zipcodes"))
            writer.writerow(station)
    print("wrote to file: %s" % output_filename)
