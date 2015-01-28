SHELL = /bin/bash

.PHONY: all firefox-work firefox-personal firefox
.DEFAULT: all

SRCDIR ?= $(abspath $(dir $(lastword $(MAKEFILE_LIST))))/

PREFIX ?= /usr/local/

BINDIR = $(PREFIX)bin/

SBINDIR = $(PREFIX)sbin/

ETCDIR = $(CONFIGDIR)

BINTARGETS ?= $(foreach bin, $(shell cat $(SRCDIR)bin.lst), $(BINDIR))

SBINTARGETS ?= $(foreach sbin, $(shell cat $(SRCDIR)sbin.lst), $(SBINDIR))

ETCTARGETS ?= $(foreach etc, $(shell cat $(SRCDIR)etc.lst), $(ETCDIR))

SHARETARGETS ?= $(foreach share, $(shell cat $(SRCDIR)share.lst), $(SHAREDIR))

DARKICETARGETS ?= $(BINDIR)darkice-media $(BINDIR)darkice-ft857d $(BINDIR)darkice-rtlsdr $(BINDIR)darkice-hackrf

$(BINDIR) $(SBINDIR) $(ETCDIR) $(SHAREDIR) $(PREFIX):
	mkdir -p $@

$(BINTARGETS): $(BINDIR)
	ln -sf $(subst $(BINDIR), $(SRCDIR), $@) $@

$(SBINTARGETS): $(SBINDIR)
	ln -sf $(subst $(SBINDIR), $(SRCDIR), $@) $@

$(ETCTARGETS): $(ETCDIR)
	ln -sf $(subst $(ETCDIR), $(SRCDIR), $@) $@

$(SHARETARGETS): $(SHAREDIR)
	ln -sf $(subst $(SHAREDIR), $(SRCDIR), $@) $@

all: $(BINTARGETS) $(SBINTARGETS) $(ETCTARGETS) $(SHARETARGETS)

firefox: $(BINDIR)firefox-anon $(BINDIR)firefox-nono $(BINDIR)firefox-default $(BINDIR)firefox-work $(BINDIR)firefox-personal

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
