#!/bin/sh

java -Dsbt.main.class=sbt.ConsoleMain -Dsbt.boot.directory=$HOME/.sbt/boot -jar sbt-launch.jar "$@"

