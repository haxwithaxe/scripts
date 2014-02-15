SHELL = /bin/bash

.PHONY: all say
.DEFAULT: all

SRCDIR ?= $(abspath $(dir $(lastword $(MAKEFILE_LIST))))/

DESTDIR ?= $(HOME)/.bin/

HOMEBIN ?= $(shell cat $(SRCDIR)bin.lst)

HOMEBIN_DEST = $(foreach bin, $(HOMEBIN), $(DESTDIR)$(bin))

$(DESTDIR):
	mkdir -p $@

$(HOMEBIN_DEST): $(DESTDIR)
	ln -sf $(subst $(DESTDIR), $(SRCDIR), $@) $@

say:
	echo $(HOMEBIN_DEST)

all: $(HOMEBIN_DEST)
