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

# find the first day of the current week
start_date = today - relativedelta(days=today.weekday())
start_date = start_date.replace(hour=0, minute=0, second=0, microsecond=0)
# add two weeks
end_date   = start_date + relativedelta(weeks=2) - relativedelta(days=1)
end_date   = end_date.replace(hour=23, minute=59, second=59, microsecond=0)

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

print(month)

# load template
template_file = open("template.shtml", "r")
template = template_file.read()
template = template.replace("${TODAY_DAY}", str(current_day))
template = template.replace("${TODAY_WEEKDAY}","AAA2")
template = template.replace("${TODAY_MONTH}","AAA3")
template = template.replace("${TODAY_YEAR}","AAA4")

# loop
template = template.replace("${TODAY_FULL_DAY_EVENTS}", "aaaaaaaa<br>")
template = template.replace("${TODAY_EVENTS}", "bbbbbbbb<br>")

# loop
row = '''\
<td style="width: 14%;">
<span style="font-size: 50px; color: {color}; text-decoration-style: wavy; text-decoration-line: {decor};">
<strong>{curday}</strong><br></span><br>
<span style="font-size: 20px; color: {color};">
<strong>{allday}<strong>
{timeday}
</span>
</td>'''


dayrow=""
loop_day = start_date
while loop_day <= end_date:
	color="black"
	decor="none"

	# TODO also detect public holiday
	if loop_day.weekday() >= 5:
		color="red"
	if loop_day.day == current_day:
		decor="underline"

	allday="UUUU<br>"
	timeday="ddddd<br>"

	if loop_day == start_date + relativedelta(weeks=1):
		dayrow+="\n</tr>\n<tr>"
	dayrow+=row.format(color=color, decor=decor, allday=allday, timeday=timeday, curday=loop_day.day)+"\n"

	loop_day += relativedelta(days=1)

template = template.replace("${DAY_ROW}", dayrow)

output_file = open(sys.argv[2], "w")
output_file.write(template)
output_file.close()
