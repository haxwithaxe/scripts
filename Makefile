SHELL = /bin/bash

.PHONY: all ham firefox noaa xsl
.DEFAULT: all


prefix ?= usr/local/
exec_prefix = $(prefix)
bindir = $(exec_prefix)bin/
sbindir = $(exec_prefix)sbin/
sysconfdir = $(prefix)etc/
datadir = $(exec_prefix)share/

SRCDIR ?= $(abspath $(dir $(lastword $(MAKEFILE_LIST))))/

DESTDIR ?= /
BINDIR = $(DESTDIR)$(bindir)
SBINDIR = $(DESTDIR)$(sbindir)
SYSCONFDIR = $(DESTDIR)$(sysconfdir)
DATADIR = $(DESTDIR)$(datadir)

DARKICETARGETS ?= $(BINDIR)darkice-media $(BINDIR)darkice-ft857d $(BINDIR)darkice-rtlsdr $(BINDIR)darkice-hackrf

DIRS = $(DESTDIR) $(BINDIR) $(SBINDIR) $(SYSCONFDIR) $(DATADIR) $(DATADIR)noaa $(DATADIR)xsl

all: firefox noaa xsl ham

ham: $(BINDIR)grig-ft857d

firefox: $(BINDIR)firefox-anon $(BINDIR)firefox-nono $(BINDIR)firefox-work $(BINDIR)firefox-personal

noaa: $(BINDIR)conky-noaa.py $(BINDIR)noaa.py $(DATADIR)noaa/stations-with-zips.csv

xsl: $(BINDIR)prettyxml $(DATADIR)xsl/prettyxml.xsl

firefox-%: $(BIINDIR)firefox-%

$(BINDIR)firefox-anon:
	ln -sf $(SRCDIR)firefox-anon $(BINDIR)firefox-anon

$(BINDIR)firefox-nono:
	ln -sf $(SRCDIR)firefox-nono $(BINDIR)firefox-nono

$(BINDIR)firefox-%:
	ln -sf $(SRCDIR)firefox-profile $(BINDIR)firefox-$*

$(BINDIR)darkice-source:
	ln -sf $(SRCDIR)darkice-source $@

$(BINDIR)darkice-%: $(BINDIR)darkice-source
	ln -sf $(BINDIR)darkice-source $@

$(BINDIR)prettyxml: $(DATADIR)xsl/prettyxml.xsl

$(DATADIR)xsl/prettyxml.xsl: $(DATADIR)xsl

$(BINDIR)conky-noaa.py $(BINDIR)noaa.py: $(DATADIR)noaa/stations-with-zips.csv

$(DATADIR)noaa/stations-with-zips.csv: $(SRCDIR)noaa/stations-with-zipcodes.csv $(DATADIR)noaa

$(SRCDIR)noaa/stations-with-zipcodes.csv:
	python $(SRCDIR)noaa_stations_with_zips.py noaa/noaa_stations.csv  noaa/zips.csv $@

$(BINDIR)%:
	ln -sf $(SRCDIR)$* $@

$(SBINDIR)%:
	ln -sf $(SRCDIR)$* $@

$(SYSCONFDIR)%:
	ln -sf $(SRCDIR)$* $@

$(DATADIR)%:
	ln -sf $(SRCDIR)$* $@

$(DIRS):
	mkdir -p $@
