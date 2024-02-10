#!/bin/bash

#BASEDIR="/path/to/store"
#ICAL_SAVE="$BASEDIR/ical.txt"
#HTML_DOC="$BASEDIR/render.html"
#PNG_SAVE="$BASEDIR/ical-raw.png"
#PNG_CROP="$BASEDIR/ical.png
#PBM_B_TEMP="$BASEDIR/ical.b.pbm"
#PBM_R_TEMP="$BASEDIR/ical.r.pbm"
#ICAL_SECRET_URL="https://calendar.google.com/calendar/ical/xxx%40group.calendar.google.com/private-xxx/basic.ics"
#EID_IP="192.168.1.1"
#EID_PORT="80"

SCRIPT=`realpath $0`
DIR=`dirname $SCRIPT`
source $DIR/.env

# headers
BCK_UP="EID0"
BCK_DN="EID1"
RED_UP="EID2"
RED_DN="EID3"
CLEAR="EID9"

# download calendar to a temp file
wget -q -O "$ICAL_SAVE" "$ICAL_SECRET_URL"

# parse and save only requsted month and the next one
python3 process_month.py "$ICAL_SAVE" "$HTML_DOC"
firefox --headless --screenshot "$PNG_SAVE" "file://$HTML_DOC" 1> /dev/null 2> /dev/null
convert "$PNG_SAVE" -crop 1304x984+12+4 "$PNG_CROP"

# convert to black
convert "$PNG_CROP" -negate "$PBM_B_TEMP"

# save only red color
convert "$PNG_CROP" -fill white +opaque red "$PBM_R_TEMP.png"
convert "$PBM_R_TEMP.png" -negate "$PBM_R_TEMP"

# clear display
cat <(echo -n $CLEAR) | nc -w 1 $EID_IP $EID_PORT
sleep 30

chunk=$((1304*984/8/2))
cat <(echo -n $BCK_UP) <(tail -n +3 "$PBM_B_TEMP" | dd bs=1 count=$chunk skip=0 2>/dev/null)      | nc -w 10 $EID_IP $EID_PORT
cat <(echo -n $BCK_DN) <(tail -n +3 "$PBM_B_TEMP" | dd bs=1 count=$chunk skip=$chunk 2>/dev/null) | nc -w 10 $EID_IP $EID_PORT
cat <(echo -n $RED_UP) <(tail -n +3 "$PBM_R_TEMP" | dd bs=1 count=$chunk skip=0 2>/dev/null)      | nc -w 10 $EID_IP $EID_PORT
cat <(echo -n $RED_DN) <(tail -n +3 "$PBM_R_TEMP" | dd bs=1 count=$chunk skip=$chunk 2>/dev/null) | nc -w 10 $EID_IP $EID_PORT

