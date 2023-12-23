#!/bin/bash

#ICAL_SAVE="/path/to/store/ical.txt"
#PNG_SAVE="/path/to/store/ical.png"
#PBM_TEMP="/path/to/store/ical.pbm"
#ICAL_SECRET_URL="https://calendar.google.com/calendar/ical/xxx%40group.calendar.google.com/private-xxx/basic.ics"
#EID_IP="192.168.1.1"
#EID_PORT="80"
source .env

HEADER0="EID0"
HEADER1="EID1"

# download calendar to a temp file
wget -q -O "$ICAL_SAVE" "$ICAL_SECRET_URL"

# parse and save only requsted month and the next one
python3 process_month.py "$ICAL_SAVE" "$PNG_SAVE"

convert "$PNG_SAVE" -crop 1304x984+124+42 -negate "$PBM_TEMP"
chunk=$((1304*984/8/2))
cat <(echo -n $HEADER0) <(tail -n +3 "$PBM_TEMP" | dd bs=1 count=$chunk skip=0 2>/dev/null)      | nc -w 5 $EID_IP $EID_PORT
cat <(echo -n $HEADER1) <(tail -n +3 "$PBM_TEMP" | dd bs=1 count=$chunk skip=$chunk 2>/dev/null) | nc -w 5 $EID_IP $EID_PORT

