FROM alpine:latest

ENV BASEDIR=/app
ENV TEMPDIR=/app/tmp

RUN mkdir -p $BASEDIR
RUN mkdir -p $TEMPDIR

COPY process_month.py $BASEDIR
COPY pull_calendar.sh $BASEDIR
COPY template.shtml   $BASEDIR
COPY style.css        $BASEDIR
COPY config.sh        $BASEDIR

RUN apk update && \
    apk add wget python3 bash netcat-openbsd py3-pip imagemagick firefox && \
    pip3 install icalendar recurring_ical_events --break-system-packages

RUN echo -e "#!/bin/bash\n\
echo 'Hello from within the Docker container'\n\
echo 'Starting cron daemon'\n\
crond -f -L /dev/stdout\n\
echo 'Cron daemon started'" > $BASEDIR/entrypoint.sh

RUN chmod +x $BASEDIR/pull_calendar.sh && \
    chmod +x $BASEDIR/entrypoint.sh

RUN > /etc/crontabs/root && \
    echo '0 * * * * /bin/bash /app/pull_calendar.sh' >> /etc/crontabs/root && \
    echo '@reboot   /bin/bash /app/pull_calendar.sh' >> /etc/crontabs/root

CMD ["/bin/bash", "/app/entrypoint.sh"]