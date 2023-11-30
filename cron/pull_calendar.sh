#!/bin/bash

#ICAL_SAVE="/path/to/store/ical.txt"
#ICAL_SECRET_URL="https://calendar.google.com/calendar/ical/xxx%40group.calendar.google.com/private-xxx/basic.ics"
#ICAL_VERSION="/path/to/store/ical-version-hash.txt"
#EID_IP="192.168.1.1"
#EID_PORT="80"
source .env

HEADER0="EID0"
HEADER1="EID1"

# save previous pull files
mv "$ICAL_SAVE"    "$ICAL_SAVE.bak"    2>/dev/null
mv "$ICAL_VERSION" "$ICAL_VERSION.bak" 2>/dev/null

# download calendar to a temp file
wget -q -O "$ICAL_SAVE.tmp" "$ICAL_SECRET_URL"

# parse and save only requsted month and the next one
python3 process_month.py "$ICAL_SAVE.tmp" > "$ICAL_SAVE"

# calc checksum
md5sum "$ICAL_SAVE" | cut -d ' ' -f 1 > "$ICAL_VERSION"

# compare checksums
curr=`cat $ICAL_VERSION`
prev=`cat $ICAL_VERSION.bak`

if [ "$curr" != "$prev" ] || [ "$1" == "force" ]
then
	# if changes have been detected - update the screen
	python3 ../ical2img/render_ical.py "$ICAL_SAVE"
	convert calplot.png -crop 1304x984+124+42 calplot.pbm
	chunk=$((1304*984/8/2))
	tail -n +3 calplot.pbm | dd bs=1 count=$chunk > calplot.0
	tail -n +3 calplot.pbm | dd bs=1 count=$chunk skip=$chunk > calplot.1
	cat <(echo -n $HEADER0) calplot.0 | nc $EID_IP $EID_PORT
	cat <(echo -n $HEADER1) calplot.1 | nc $EID_IP $EID_PORT
fi

# cleanup
rm "$ICAL_SAVE.tmp"

