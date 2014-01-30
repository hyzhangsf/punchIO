#!/usr/bin/env bash

# set exit on error
set -e
#the path for this punchIO
DESTINATION="/usr/local/bin/"
# the path for db
# db="/usr/local/share/punch/example.db"
# check if $DESTINATION exists
if [ -d $DESTINATION ]; then
	cp ../punchInRecorder.py $DESTINATION/punch
	chmod 777 $DESTINATION/punch
fi
