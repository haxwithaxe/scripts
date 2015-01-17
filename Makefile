SHELL = /bin/bash

.PHONY: all say firefox-work firefox-personal
.DEFAULT: all

SRCDIR ?= $(abspath $(dir $(lastword $(MAKEFILE_LIST))))/

DESTDIR ?= $(HOME)/.local/

HOMEBIN ?= $(shell cat $(SRCDIR)bin.lst)

HOMEBIN_DEST = $(foreach bin, $(HOMEBIN), $(DESTDIR)$(bin))

$(DESTDIR):
	mkdir -p $@

$(HOMEBIN_DEST): $(DESTDIR)
	ln -sf $(subst $(DESTDIR), $(SRCDIR), $@) $@

say:
	echo $(HOMEBIN_DEST)

all: $(HOMEBIN_DEST)

firefox-work:
	ln -s $(SRCDIR)/firefox-default /usr/local/bin/firefox-work
	ln -s $(SRCDIR)/firefox-profile /usr/local/bin/firefox-default
	ln -s $(SRCDIR)/firefox-profile /usr/local/bin/firefox-personal

firefox-personal:
	ln -s $(SRCDIR)/firefox-default /usr/local/bin/firefox-personal
	ln -s $(SRCDIR)/firefox-profile /usr/local/bin/firefox-default
	ln -s $(SRCDIR)/firefox-profile /usr/local/bin/firefox-work

