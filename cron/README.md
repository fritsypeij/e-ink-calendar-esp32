# Prereqs

For Ubuntu:

```
sudo apt install wget python3 python3-pip imagemagick netcat firefox language-pack-lt
sudo pip3 install icalendar recurring_ical_events
```
Note, Ubuntu may also aks you to run `sudo snap install firefox`, check terminal output.

For Alpine:

```
apk update
apk add wget python3 bash netcat-openbsd py3-pip imagemagick firefox
```

# Env file

Create `.env` file with your real Google magic link and display's address, ex:

```
ICAL_SECRET_URL="https://calendar.google.com/calendar/ical/xxx%40group.calendar.google.com/private-xxx/basic.ics"
EID_IP="192.168.1.1"
EID_PORT="80"
```

# Cron

Add this line to your cron:

```
0 0 * * * cd /path/to/git/e-ink-calendar-esp32/cron && ./pull_calendar.sh
```

# Docker

Optionally, you can run script in docker.

To build, run `build_docker.sh`.

To run:

```
docker run -ti calendar
```
