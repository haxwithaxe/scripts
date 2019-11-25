SHELL = /bin/bash

.PHONY: all ham firefox chrome noaa xrandr-setup xsl
.DEFAULT: all


prefix ?= 
exec_prefix = $(prefix)
bindir = $(exec_prefix)bin/
sbindir = $(exec_prefix)sbin/
datadir = $(exec_prefix)share/

SRCDIR ?= $(abspath $(dir $(lastword $(MAKEFILE_LIST))))/

DESTDIR ?= $(HOME)/.local/
BINDIR = $(DESTDIR)$(bindir)
SBINDIR = $(DESTDIR)$(sbindir)
SYSCONFDIR = $(HOME)/.config/
DATADIR = $(DESTDIR)$(datadir)

DARKICETARGETS ?= $(BINDIR)darkice-media $(BINDIR)darkice-ft857d $(BINDIR)darkice-rtlsdr $(BINDIR)darkice-hackrf

DIRS = $(DESTDIR) $(BINDIR) $(SBINDIR) $(SYSCONFDIR) $(DATADIR) $(DATADIR)noaa $(DATADIR)xsl

all: firefox ham

acpi: $(BINDIR)acpi-listener

ham: $(BINDIR)grig-ft857d

firefox: $(BINDIR)firefox-anon $(BINDIR)firefox-nono $(BINDIR)firefox-work $(BINDIR)firefox-personal

chrome: $(BINDIR)chrome-anon $(BINDIR)chrome-nono $(BINDIR)chrome-work $(BINDIR)chrome-personal

noaa: $(BINDIR)conky-noaa.py $(BINDIR)noaa.py $(DATADIR)noaa/stations-with-zips.csv

xsl: $(BINDIR)prettyxml $(DATADIR)xsl/prettyxml.xsl

prettyprinters: prettyxml prettyjson

prettyxml: $(BINDIR)prettyxml

prettyjson: $(BINDIR)prettyjson

firefox-%: $(BINDIR)firefox-%

chrome-%: $(BINDIR)chrome-%

$(BINDIR)chrome-anon:
	ln -sf $(SRCDIR)chrome-anon $(BINDIR)chrome-anon

$(BINDIR)chrome-anon-proxy:
	ln -sf $(SRCDIR)chrome-anon-proxy $(BINDIR)chrome-anon-proxy

$(BINDIR)firefox-anon:
	ln -sf $(SRCDIR)firefox-anon $(BINDIR)firefox-anon

$(BINDIR)firefox-nono:
	ln -sf $(SRCDIR)firefox-nono $(BINDIR)firefox-nono

$(BINDIR)firefox-%:
	ln -sf $(SRCDIR)firefox-$* $(BINDIR)firefox-$*

$(BINDIR)chrome-%:
	ln -sf $(SRCDIR)chrome-$* $(BINDIR)chrome-$*

$(BINDIR)darkice-source:
	ln -sf $(SRCDIR)darkice-source $@

$(BINDIR)darkice-%: $(BINDIR)darkice-source
	ln -sf $(BINDIR)darkice-source $@

$(BINDIR)prettyxml: $(DATADIR)xsl/prettyxml.xsl

$(DATADIR)xsl/prettyxml.xsl: $(DATADIR)xsl

$(BINDIR)conky-noaa.py $(BINDIR)noaa.py: $(DATADIR)noaa/stations-with-zips.csv

$(DATADIR)noaa/stations-with-zips.csv: $(SRCDIR)noaa/stations-with-zipcodes.csv $(DATADIR)noaa

$(BINDIR)acpi-listener: $(BINDIR)tosocket

$(SRCDIR)noaa/stations-with-zipcodes.csv:
	python2 $(SRCDIR)noaa_stations_with_zips.py noaa/noaa_stations.csv  noaa/zips.csv $@

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
