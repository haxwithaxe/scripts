#!/usr/bin/env python2
""" Attach zipcodes that have a station closest to it to that station. """

__authors__ = ['haxwithaxe me@haxwithaxe.net']

__license__ = 'GPLv3'

import csv
import re
import logging as logger

logger.basicConfig(level=logger.INFO)

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
        """ Empty docstring. """
        # stations => {'id':entry}
        with open(filename, "rb") as stacsv:
            dialect = csv.Sniffer().sniff(stacsv.read(1024))
            stacsv.seek(0)
            stations_db = csv.DictReader(stacsv,
                                         fieldnames=self.station_headers,
                                         dialect=dialect)
            for station in stations_db:
                lat = station.get('lat')
                lon = station.get('lon')
                logger.debug("orig: %s, %s", lat, lon)
                declat = self._coord_to_decdeg(lat)
                declon = self._coord_to_decdeg(lon)
                logger.debug("decimal cood: %s, %s", declat, declon)
                station.update({'lat': declat, 'lon': declon, "zipcodes":[]})
                logger.debug("contry: %s; cood: %s, %s", station.get("co"), station.get("lat"), station.get("lon"))
                self.stations.update({station.get('ind'): station})

    def _load_zipcodes(self, filename):
        """ Empty docstring. """
        with open(filename, "r") as zipcsv:
            dialect = csv.Sniffer().sniff(zipcsv.read(1024))
            zipcsv.seek(0)
            zipcodes_db = csv.DictReader(zipcsv, fieldnames=self.zip_headers,
                                         dialect=dialect)
            for zipcode in zipcodes_db:
                zipcode.update({"lat": float(zipcode.get("lat")),
                                "lon": float(zipcode.get("lon"))})
                self.zipcodes.append(zipcode)

    def get_db(self):
        """ Empty docstring. """
        self.zips_for_stations()
        return self.stations

    def zips_for_stations(self):
        """ Iterate over zipcodes and attach them to satations """
        for zipcode in self.zipcodes:
            self.zip_for_station(zipcode)

    def zip_to_station(self, zipcode):
        """ Find the station closest to the zipcode """
        best_dist, best_sta = 99999999, ''
        for sta_id, station in self.stations.items():
            tlat, tlon = station.get('lat'), station.get('lon')
            distance = ((tlat-zipcode.get('lat'))**2 +
                        (tlon-zipcode.get('lon'))**2)**0.5
            if distance < best_dist:
                best_dist, best_sta = distance, sta_id
        logger.debug("zipcode: %s, station:%s",
                     zipcode.get("zip", "no zipcode"), best_sta)
        return best_sta

    def zip_for_station(self, zipcode):
        """ Attach the zipcode to the station closest to it. """
        station = self.zip_to_station(zipcode)
        self.stations[station]['zipcodes'].append(zipcode.get("zip"))
        logger.debug(self.stations[station].get('zipcodes', 'no zipcodes'))

    def _coord_to_decdeg(self, coord_str):
        """ Return decimal representation of DMS. """
        coord = Coord(coord_str)
        return coord.decimal()

class Coord(object):

    def __init__(self, coord_str):
        logger.debug(coord_str)
        self.string = coord_str.strip()
        self.chunks = (["degree",0.0], ["minute", 0.0], ["second", 0.0], ["frac_seconds", 0.0])
        self._strip()
        self._sign()

    def _strip(self):
        self.string = re.sub(r'\s', '', self.string)

    def _sign(self):
        if re.search('[sw]', self.string, re.I):
            logger.debug("coord: %s, sign: -")
            self.sign = -1
        else:
            logger.debug("coord: %s, sign: +")
            self.sign = 1

    def _split_degminsec(self):
        diced = re.split('\D+', self.string, maxsplit=4)
        logger.debug("diced coord: %s", diced)
        count = len(self.chunks)
        if len(diced)-len(self.chunks) < 0:
            count = len(diced)
        i = 0
        while i < count:
            self.chunks[i][1] = diced[i]
            i+=1
        logger.debug("chuncks of coord: %s", self.chunks)

    def decimal(self):
        self._split_degminsec()
        cdict = dict(self.chunks)
        logger.debug("chuncks dict: %s", cdict)
        return self.sign * (int(cdict["degree"] or 0) + float(cdict["minute"] or 0) / 60 + float(cdict["second"] or 0) / 3600 + float(cdict["frac_seconds"] or 0) / 36000)


if __name__ == '__main__':
    import sys
    sta_filename = sys.argv[1]
    zip_filename = sys.argv[2]
    output_filename = sys.argv[3]
    sta_db = StationsDB(sta_filename, zip_filename).get_db()
    with open(output_filename, 'w') as csvfile:
        writer = csv.DictWriter(csvfile,
                                fieldnames=list(sta_db.values()[0].keys()))
        writer.writeheader()
        for sta in sta_db.values():
            logger.debug("final zipcodes for %s, %s, %s: %s",
                         sta.get("ind"),
                         sta.get("stabv"),
                         sta.get("co"),
                         len( sta.get('zipcodes', ['no zipcodes']) ) )
            sta["zipcodes"] = ";".join(sta.get("zipcodes"))
            logger.debug("zipcodes: %s", sta.get("zipcodes"))
            writer.writerow(sta)
    print("wrote to file: %s" % output_filename)
