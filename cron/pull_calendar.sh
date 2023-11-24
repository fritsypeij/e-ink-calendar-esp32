#!/bin/bash

#ICAL_SAVE="/path/to/store/ical.txt"
#ICAL_SECRET_URL="https://calendar.google.com/calendar/ical/xxx%40group.calendar.google.com/private-xxx/basic.ics"
#ICAL_VERSION="/path/to/store/ical-version-hash.txt"

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

if [ "$curr" != "$prev" ]
then
	# if changes have been detected - update the screen
	python3 render_ical.py "$ICAL_SAVE"
	convert calplot.png calplot.pbm

fi

# cleanup
rm "$ICAL_SAVE.tmp"

