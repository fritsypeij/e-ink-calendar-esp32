import icalendar
from icalendar import Calendar
from datetime import datetime, timezone
from dateutil.relativedelta import relativedelta
import pytz
import sys

mytz = pytz.UTC

input_file = open(sys.argv[1], "r")
ical_events = Calendar().from_ical(input_file.read())

start_date = datetime.today().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
end_date = start_date + relativedelta(months=1) + relativedelta(weeks=1)
start_date = mytz.localize(start_date)
end_date = mytz.localize(end_date)

month = dict()
for event in ical_events.walk():

	if event.name == "VEVENT":

		cal_date = event.get('dtstart').dt
		event_date = datetime.combine(cal_date, datetime.min.time())
		if event_date.tzinfo == None:
			event_date = mytz.localize(event_date)

		if event_date > start_date and event_date < end_date:

			if event_date.day not in month:
				month[event_date.day] = list()

			# check for full day event
			delta = event.get('dtend').dt - event.get('dtstart').dt
			if delta.days >= 1:
				for i in range(0, delta.days):
					month[event_date.day + i].append([None, event.get('summary')])
			else:
				month[event_date.day].append([event_date, event.get('summary')])

for day in month:
	print(day, month[day])

