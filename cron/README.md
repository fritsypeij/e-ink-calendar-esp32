# Docker (Dockerfile):

This guide is for those who want to have a quick and easy setup. The following commands will create a docker container based on Alpine Linux and install the necessary packages.

Create the `config.sh` file based on the provided `config.sh.sample` file. This file contains the necessary configuration for the calendar to work.

Create a folder on your host machine and copy the following files into it:

``` bash
config.sh # Create this file based on config.sh.sample
process_month.py
pull_calendar.sh
style.css
template.shtml
Dockerfile
```

Grab your favorite terminal, create, start and connect to an Alpine docker container with the following commands:

``` bash
docker build -t calendar .
docker run -d --restart=always -v /path/on/host:/app -e BASEDIR=/app -e TEMPDIR=/app/temp --name calendar calendar crond -f
```

# Docker (manually):

Manually create a docker container based on Alpine Linux and install the necessary packages. This guide is for those who want to have more control over the installation process.

Create the `config.sh` file based on the provided `config.sh.sample` file. This file contains the necessary configuration for the calendar to work.

Create a folder on your host machine and copy the following files into it:

``` bash
config.sh # Create this file based on config.sh.sample
process_month.py
pull_calendar.sh
style.css
template.shtml
```

Grab your favorite terminal, create, start and connect an Alpine docker container with the following commands:

``` bash
docker run -d --restart=always -v /path/on/host:/app -e BASEDIR=/app -e TEMPDIR=/app/temp --name calendar alpine:latest crond -f
docker exec -it calendar bin/ash
```

You're now connected to your new docker container. Run the following commands to install the necessary packages:

``` bash
apk update
apk add nano wget python3 bash netcat-openbsd py3-pip imagemagick firefox
pip3 install icalendar recurring_ical_events --break-system-packages
```

## Cron

1) Open the crontab file:
   ``` bash
   crontab -e
   ```
2) Add the following line to run pull_calendar.sh every hour:
   ``` bash
   0 * * * * /app/pull_calendar.sh
   ```
   To update the calendar on other intervals, check out this [cron cheatsheet](https://devhints.io/cron).
3) Save and exit (In nano, press `Ctrl+X`, then `Y`, then `Enter`).

Alternatively, you can use Alpine's periodic cron folders inside `/etc/periodic/`. Add a bash script to one of the predefined folders that executes `/app/pull_calendar.sh`.

Exit the container shell with `exit` and then restart the container with `docker restart calendar`.


# Ubuntu:

``` bash
sudo apt install wget python3 python3-pip imagemagick netcat firefox language-pack-lt
sudo pip3 install icalendar recurring_ical_events
```
Note, Ubuntu may also aks you to run `sudo snap install firefox`, check terminal output.

## Cron

Run `crontab -e` to edit the cron file.
Add these lines to update the display hourly:

``` bash
0 * * * * /bin/bash /path/to/pull_calendar.sh
```

To update the calendar on other intervals, check out this [cron cheatsheet](https://devhints.io/cron).
