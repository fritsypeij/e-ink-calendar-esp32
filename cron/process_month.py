import icalendar
from icalendar import Calendar
from datetime import datetime, timezone
from dateutil.relativedelta import relativedelta
import pytz
import sys
import json

def append_event(idx, dt, ev):
	global month
	if idx not in month:
		month[idx] = list()
	month[idx].append([dt, ev])

mytz = pytz.UTC

input_file = open(sys.argv[1], "r")
ical_events = Calendar().from_ical(input_file.read())

# get the first day of the current month
start_date = datetime.today().replace(day=1, hour=0, minute=0, second=0, microsecond=0)

# include one week of the previous and the next months
end_date   = start_date + relativedelta(weeks=1) + relativedelta(months=1)
start_date = start_date - relativedelta(weeks=1)
start_date = mytz.localize(start_date)
end_date   = mytz.localize(end_date)

month = dict()
for event in ical_events.walk():

	if event.name != "VEVENT":
		continue

	cal_date = event.get('dtstart').dt
	event_date = datetime.combine(cal_date, datetime.min.time())
	if event_date.tzinfo == None:
		event_date = mytz.localize(event_date)

	if event_date > start_date and event_date < end_date:
		dayindex = int(event_date.strftime('%Y%m%d'))
		summary = str(event.get('summary'))

		# check for full day event
		delta = event.get('dtend').dt - cal_date
		if delta.days >= 1:
			for i in range(0, delta.days):
				append_event(dayindex + i, None, summary)
		else:
			append_event(dayindex, cal_date.strftime('%H%M'), summary)

for day in month:
	print(day, month[day])

print(json.dumps(month))
