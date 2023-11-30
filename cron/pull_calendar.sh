#!/bin/bash

#ICAL_SAVE="/path/to/store/ical.txt"
#ICAL_SECRET_URL="https://calendar.google.com/calendar/ical/xxx%40group.calendar.google.com/private-xxx/basic.ics"
#EID_IP="192.168.1.1"
#EID_PORT="80"
source .env

HEADER0="EID0"
HEADER1="EID1"

# download calendar to a temp file
wget -q -O "$ICAL_SAVE" "$ICAL_SECRET_URL"

# parse and save only requsted month and the next one
python3 process_month.py "$ICAL_SAVE"

convert calplot.png -crop 1304x984+124+42 calplot.pbm
chunk=$((1304*984/8/2))
tail -n +3 calplot.pbm | dd bs=1 count=$chunk skip=0      > calplot.0 2> /dev/null
tail -n +3 calplot.pbm | dd bs=1 count=$chunk skip=$chunk > calplot.1 2> /dev/null
cat <(echo -n $HEADER0) calplot.0 | nc -w 5 $EID_IP $EID_PORT
cat <(echo -n $HEADER1) calplot.1 | nc -w 5 $EID_IP $EID_PORT

