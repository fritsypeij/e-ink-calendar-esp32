#!/bin/bash

log_error ()
{
	echo "$1"
	log_info "$1"
}

log_info ()
{
	logger "$0: $1"
}

# get script's dir
SCRIPT=`realpath $0`
DIR=`dirname $SCRIPT`

# if env does not override, use the script's dir
if [ -z "$BASEDIR" ]
then
	log_info "BASEDIR not defined, setting to $DIR"
	BASEDIR=$DIR
	TEMPDIR=$DIR/tmp

	# Create the directory if it doesn't exist
	mkdir -p $TEMPDIR
fi

# file locations
ICAL_SAVE="$TEMPDIR/ical.txt"
HTML_TEMPLATE="$BASEDIR/template.shtml"
HTML_RENDER="$TEMPDIR/render.html"
PNG_SAVE="$TEMPDIR/ical-raw.png"
PNG_CROP="$TEMPDIR/ical-crop.png"
PBM_TEMP="$TEMPDIR/ical.png"
PBM_B_TEMP="$TEMPDIR/ical.b.pbm"
PBM_R_TEMP="$TEMPDIR/ical.r.pbm"
PALETTE="$TEMPDIR/palette.gif"
CONFIG="$BASEDIR/config.sh"

source $CONFIG

# headers
BCK_UP="EID0"
BCK_DN="EID1"
RED_UP="EID2"
RED_DN="EID3"
CLEAR="EID9"

log_info "download calendar to a temp file"
> "$ICAL_SAVE"

# Loop over the URLs
for url in "${ICAL_SECRET_URLS[@]}"; do
    # Download the calendar and append it to the file
    wget -q -O - "$url" >> "$ICAL_SAVE"
    if [ $? != 0 ]; then
        echo "Unable to download the calendar from $url"
        exit 1
    fi
done

if [ ! -s "$ICAL_SAVE" ]; then
    echo "No calendars were downloaded"
    exit 1
fi

log_info "parse and save only requsted month and the next one"
python3 "$BASEDIR/process_month.py" "$ICAL_SAVE" "$HTML_TEMPLATE" "$HTML_RENDER" $1
if [ $? != 0 ]
then
	log_error "python code failed"
	exit 10
fi

log_info "detect firefox"
firefox --version > /dev/null
if [ $? != 0 ]
then
	log_error "Unable to run headless firefox"
	exit 2
fi

log_info "run firefox to make screenshot only"
firefox --headless --screenshot "$PNG_SAVE" "file://$HTML_RENDER" 1> /dev/null 2> /dev/null
log_info "crop area that fits our screen"
convert "$PNG_SAVE" -crop 1304x984+0+0 "$PNG_CROP"
if [ $? != 0 ]
then
	log_error "Unable to crop PNG"
	exit 3
fi

log_info "converting to black-red-white"
convert xc:black xc:white xc:red +append "$PALETTE"
convert "$PNG_CROP" -dither FloydSteinberg -remap "$PALETTE" "$PBM_TEMP"

log_info "extract red and black colors to separate files"
convert "$PBM_TEMP" -fill white -opaque red -negate "$PBM_B_TEMP"
convert "$PBM_TEMP" -fill white -opaque black -negate "$PBM_R_TEMP"

log_info "clear display"
cat <(echo -n $CLEAR) | nc -w 1 $EID_IP $EID_PORT

sleep 60

chunk=$((1304*984/8/2))
log_info "sending black top"
cat <(echo -n $BCK_UP) <(tail -n +3 "$PBM_B_TEMP" | dd bs=1 count=$chunk skip=0 2>/dev/null)      | nc -w 10 $EID_IP $EID_PORT
log_info "sending black bottom"
cat <(echo -n $BCK_DN) <(tail -n +3 "$PBM_B_TEMP" | dd bs=1 count=$chunk skip=$chunk 2>/dev/null) | nc -w 10 $EID_IP $EID_PORT
log_info "sending red up"
cat <(echo -n $RED_UP) <(tail -n +3 "$PBM_R_TEMP" | dd bs=1 count=$chunk skip=0 2>/dev/null)      | nc -w 10 $EID_IP $EID_PORT
log_info "sending red down"
cat <(echo -n $RED_DN) <(tail -n +3 "$PBM_R_TEMP" | dd bs=1 count=$chunk skip=$chunk 2>/dev/null) | nc -w 10 $EID_IP $EID_PORT

log_info "done"

