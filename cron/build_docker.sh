#!/bin/bash -e

source .env

docker build \
	--build-arg ICAL_SECRET_URL="$ICAL_SECRET_URL" \
	--build-arg EID_IP="$EID_IP" \
	--build-arg EID_PORT="$EID_PORT" \
	-t calendar .

