import icalendar
from icalendar import Calendar
from datetime import datetime, timezone
from dateutil.relativedelta import relativedelta
import pytz
import sys

def append_event(idx, dt, ev):
	global month
	if idx not in month:
		month[idx] = list()
	month[idx].append([dt, ev])


mytz = pytz.timezone("Europe/Vilnius")

input_file = open(sys.argv[1], "r")
ical_events = Calendar().from_ical(input_file.read())

# today
today = datetime.today()
current_day   = today.day
current_month = today.month
current_year  = today.year

# get the first day of the current month
start_date = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

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
			localtime = cal_date.astimezone(mytz).strftime("%H%M")
			append_event(dayindex, localtime, summary)


for day in month:
	for event in month[day]:
		summary = event[1]
		recover_day = int(str(day)[-2:])
		recover_month = int(str(day)[-4:-2])
		if recover_month != current_month:
			continue
		if event[0]:
			summary = event[0] + " " + summary
		print(recover_day, summary)

# write html to sys.argv[2]


