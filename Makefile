SHELL = /bin/bash

.PHONY: all firefox-work firefox-personal firefox jackd noaa xsl
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

BINTARGETS ?= $(sort $(foreach bin, $(shell cat $(SRCDIR)bin.lst), $(BINDIR)$(bin)))
SBINTARGETS ?= $(sort $(foreach sbin, $(shell cat $(SRCDIR)sbin.lst), $(SBINDIR)$(sbin)))
SYSCONFTARGETS ?= $(sort $(foreach etc, $(shell cat $(SRCDIR)etc.lst), $(SYSCONFDIR)$(etc)))
DATATARGETS ?= $(sort $(foreach share, $(shell cat $(SRCDIR)share.lst), $(DATADIR)$(share)))
DARKICETARGETS ?= $(BINDIR)darkice-media $(BINDIR)darkice-ft857d $(BINDIR)darkice-rtlsdr $(BINDIR)darkice-hackrf

$(BINDIR) $(SBINDIR) $(SYSCONFDIR) $(DATADIR) $(DESTDIR):
	mkdir -p $@

$(BINTARGETS): $(BINDIR)
	ln -sf $(subst $(BINDIR), $(SRCDIR), $@) $@

$(SBINTARGETS): $(SBINDIR)
	ln -sf $(subst $(SBINDIR), $(SRCDIR), $@) $@

$(SYSCONFTARGETS): $(SYSCONFDIR)
	ln -sf $(subst $(SYSCONFDIR), $(SRCDIR), $@) $@

$(DATATARGETS): $(DATADIR)
	ln -sf $(subst $(DATADIR), $(SRCDIR), $@) $@

all: $(BINTARGETS) $(SBINTARGETS) $(SYSCONFTARGETS) $(DATATARGETS)

firefox: $(BINDIR)firefox-anon $(BINDIR)firefox-nono $(BINDIR)firefox-default $(BINDIR)firefox-work $(BINDIR)firefox-personal

noaa: $(BINDIR)conky-noaa.py $(BINDIR)noaa.py: $(DATADIR)noaa/stations-with-zips.csv

xsl: $(BINDIR)prettyxml $(DATADIR)xsl/prettyxml.xsl

jackd: $(BINDIR)jackd-audioadapters

$(BINDIR)firefox-anon:
	ln -sf $(SRCDIR)firefox-anon $(BINDIR)firefox-anon

$(BINDIR)firefox-nono:
	ln -sf $(SRCDIR)firefox-nono $(BINDIR)firefox-nono

$(BINDIR)firefox-default:
	ln -sf $(SRCDIR)firefox-profile $(BINDIR)firefox-default

# depend on this for firefox-personal
$(BINDIR)firefox-work:
	ln -sf $(SRCDIR)firefox-profile $(BINDIR)firefox-work

# depend on this for firefox-work
$(BINDIR)firefox-personal:
	ln -sf $(SRCDIR)firefox-profile $(BINDIR)firefox-personal

firefox-work: firefox
	ln -sf $(SRCDIR)firefox-default $(BINDIR)firefox-work

firefox-personal: firefox
	ln -sf $(SRCDIR)firefox-default $(BINDIR)firefox-personal

$(DARKICETARGETS): $(BINDIR)darkice-source
	ln -sf $(BINDIR)darkice-source $@

$(BINDIR)conky-noaa.py $(BINDIR)noaa.py: $(DATADIR)noaa/stations-with-zips.csv
	ln -sf $(subst $(BINDIR), $(SRCDIR), $@) $@

$(DATADIR)noaa/stations-with-zips.csv: $(DATADIR)noaa/
	ln -sf $(subst $(DATADIR), $(SRCDIR), $@) $@

$(BINDIR)prettyxml: $(DATADIR)xsl/
	ln -sf $(subst $(DATADIR), $(SRCDIR), $@) $@

$(BINDIR)jackd-audioadapters:
	ln -sf $(subst $(BINDIR), $(SRCDIR), $@) $@

$(SRCDIR)noaa/stations-with-zipcodes.csv:
	python $(SRCDIR)noaa_stations_with_zips.py noaa/noaa_stations.csv  noaa/zips.csv $@

