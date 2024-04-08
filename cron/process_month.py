import recurring_ical_events
from icalendar import Calendar
from datetime import datetime, timedelta
import pytz
import locale
import sys
import re

def append_event(idx, dt, ev, uid, cal_name):
  global month
  if idx not in month:
    month[idx] = list()
  month[idx].append([dt, ev, uid, cal_name])

def date_idx(d):
  return d.year*10000 + d.month*100 + d.day

birthday_icon = '<svg xmlns="http://www.w3.org/2000/svg" class="icon" viewBox="0 0 24 24"><path d="M 6 0 C 6 0 4 2.895 4 4 C 4 5.105 4.895 6 6 6 C 7.105 6 8 5.105 8 4 C 8 2.895 6 0 6 0 z M 12 0 C 12 0 10 2.895 10 4 C 10 5.105 10.895 6 12 6 C 13.105 6 14 5.105 14 4 C 14 2.895 12 0 12 0 z M 18 0 C 18 0 16 2.895 16 4 C 16 5.105 16.895 6 18 6 C 19.105 6 20 5.105 20 4 C 20 2.895 18 0 18 0 z M 5 7 L 5 9.1835938 C 3.8387486 9.5978609 3 10.698391 3 12 L 3 21 C 3 21.552 3.448 22 4 22 L 20 22 C 20.552 22 21 21.552 21 21 L 21 12 C 21 10.698391 20.161251 9.5978609 19 9.1835938 L 19 7 L 17 7 L 17 9 L 13 9 L 13 7 L 11 7 L 11 9 L 7 9 L 7 7 L 5 7 z M 6 11 L 18 11 C 18.551 11 19 11.449 19 12 L 19 14.958984 C 18.437937 14.9627 17.874705 14.750719 17.494141 14.316406 L 15.5 12.037109 L 13.505859 14.316406 C 12.745859 15.184406 11.254141 15.184406 10.494141 14.316406 L 8.5 12.037109 L 6.5058594 14.316406 C 6.1252949 14.751337 5.5620629 14.962901 5 14.958984 L 5 12 C 5 11.449 5.449 11 6 11 z M 8.5 15.074219 L 8.9902344 15.634766 C 9.7502344 16.502766 10.847 17 12 17 C 13.153 17 14.249766 16.502766 15.009766 15.634766 L 15.5 15.074219 L 15.990234 15.634766 C 16.750234 16.502766 17.847 17 19 17 L 19 20 L 5 20 L 5 17 C 6.153 17 7.2497656 16.502766 8.0097656 15.634766 L 8.5 15.074219 z"></path></svg>'
all_day_icon = '<svg xmlns="http://www.w3.org/2000/svg" class="icon" viewBox="0 0 24 24"><path d="M 12 2 C 8.9883724 2 6.3037203 3.3556682 4.4707031 5.4707031 L 2 3 L 2 9 L 8 9 L 5.8769531 6.8769531 C 7.3450482 5.1245479 9.5396099 4 12 4 C 16.411 4 20 7.589 20 12 L 22 12 C 22 6.486 17.514 2 12 2 z M 2 12 C 2 16.091 4.474 19.607297 8 21.154297 L 8 18.910156 C 5.613 17.526156 4 14.952 4 12 L 2 12 z M 12.5 14 C 11.130937 14 10 15.130937 10 16.5 L 10 17 L 12 17 L 12 16.5 C 12 16.213063 12.213063 16 12.5 16 C 12.786937 16 13 16.213063 13 16.5 C 13 16.757858 12.652593 17.557212 12.082031 18.298828 C 11.511469 19.040445 10.791372 19.762633 10.314453 20.210938 L 10 20.507812 L 10 22 L 15 22 L 15 20 L 13.222656 20 C 13.381275 19.814548 13.515452 19.715819 13.667969 19.517578 C 14.347407 18.634445 15 17.683142 15 16.5 C 15 15.130937 13.869063 14 12.5 14 z M 17 14 L 17 20 L 20 20 L 20 22 L 22 22 L 22 14 L 20 14 L 20 18 L 19 18 L 19 14 L 17 14 z"></path></svg>'
confetti_icon = '<svg xmlns="http://www.w3.org/2000/svg" class="icon" viewBox="0 0 24 24"><path d="M 21.980469 1.9902344 A 1.0001 1.0001 0 0 0 21.292969 2.2929688 L 20.292969 3.2929688 A 1.0001 1.0001 0 0 0 20.001953 4 L 20.001953 5.5 L 18.501953 5.5 A 1.0001 1.0001 0 0 0 17.501953 6.5 L 17.501953 8 L 16.001953 8 A 1.0001 1.0001 0 0 0 15.292969 8.2929688 L 13.292969 10.292969 A 1.0005836 1.0005836 0 1 0 14.708984 11.707031 L 16.416016 10 L 18.501953 10 A 1.0001 1.0001 0 0 0 19.501953 9 L 19.501953 7.5 L 21.001953 7.5 A 1.0001 1.0001 0 0 0 22.001953 6.5 L 22.001953 4.4140625 L 22.708984 3.7070312 A 1.0001 1.0001 0 0 0 21.980469 1.9902344 z M 8.0019531 2 A 1.0001 1.0001 0 1 0 8.0019531 4 L 8.0117188 4 C 8.5392758 4 9.0439968 4.2094242 9.4179688 4.5820312 C 9.7906696 4.9547321 10.001953 5.4600985 10.001953 5.9882812 L 10.001953 8 A 1.0001 1.0001 0 1 0 12.001953 8 L 12.001953 5.9882812 C 12.001953 4.9304641 11.581283 3.9152679 10.833984 3.1679688 A 1.0001 1.0001 0 0 0 10.832031 3.1679688 C 10.084179 2.4214068 9.0695358 2 8.0117188 2 L 8.0019531 2 z M 15.001953 2 A 1 1 0 0 0 15.001953 4 A 1 1 0 0 0 15.001953 2 z M 5.0019531 5 A 1 1 0 0 0 5.0019531 7 A 1 1 0 0 0 5.0019531 5 z M 7.9902344 8.9902344 A 1.0001 1.0001 0 0 0 7.2929688 10.707031 L 7.5859375 11 L 3.0019531 22 L 14.001953 17.416016 L 14.292969 17.707031 A 1.0005836 1.0005836 0 1 0 15.708984 16.292969 L 8.7089844 9.2929688 A 1.0001 1.0001 0 0 0 7.9902344 8.9902344 z M 3.0019531 9 A 1 1 0 0 0 3.0019531 11 A 1 1 0 0 0 3.0019531 9 z M 22.001953 9 A 1 1 0 0 0 22.001953 11 A 1 1 0 0 0 22.001953 9 z M 8.8769531 12.291016 L 12.710938 16.125 L 6.0039062 19 L 8.8769531 12.291016 z M 16.001953 13 A 1.0001 1.0001 0 1 0 16.001953 15 L 17.976562 15 C 18.513392 15 19.028684 15.214231 19.408203 15.59375 C 19.787722 15.973269 20.001953 16.488561 20.001953 17.025391 L 20.001953 18 A 1.0001 1.0001 0 1 0 22.001953 18 L 22.001953 17.025391 C 22.001953 15.95822 21.576747 14.934168 20.822266 14.179688 C 20.067785 13.425207 19.043733 13 17.976562 13 L 16.001953 13 z M 18.001953 20 A 1 1 0 0 0 18.001953 22 A 1 1 0 0 0 18.001953 20 z"></path></svg>'

t_allday = 'hele dag' # all-day event
t_nothing_planned = confetti_icon + 'Er staat niks gepland voor vandaag!' # nothing has been planned for today

special_calendars = [
  { 
    'name': 'feestdagen',
  # 'label': confetti_icon,
    'label': 'feestdag',
  },
  { 
    'name': 'verjaardagen',
  # 'label': birthday_icon,
    'label': 'verjaardag',
  },
  {
    'name': 'vergaderingen',
    'label': 'vergadering',
  },
  {
    'name': 'vakanties',
    'label': 'vakantie',
  },
  {
    'name': 'verlof',
    'label': 'verlof',
  },
]

locale.setlocale(locale.LC_ALL, 'nl_NL')
mytz = pytz.timezone("Europe/Amsterdam")

input_file = open(sys.argv[1], "r")
ical_data = input_file.read()
calendars = re.split(r'BEGIN:VCALENDAR\r?\n', ical_data)
calendars.pop(0) # remove the first element, it is empty

ical_events = []

for calendar in calendars:
  events = Calendar.from_ical("BEGIN:VCALENDAR\n" + calendar)
  # add the X-WR-CALNAME to all events
  for event in events.walk():
    if event.name == "VEVENT":
      event.add('cal_name', events.get('x-wr-calname').lower())
  ical_events.append(events)

# today
today = datetime.today()
# today = datetime.today() + timedelta(days= -1) # for testing purposes
now = datetime.now(pytz.UTC)
current_day   = today.day
current_month = today.month
current_year  = today.year

# find the first day of the current week
start_date = today - timedelta(days=today.weekday())
start_date = start_date.replace(hour=0, minute=0, second=0, microsecond=0)
# add three weeks
end_date   = start_date + timedelta(weeks=3) - timedelta(days=1)
end_date   = end_date.replace(hour=23, minute=59, second=59, microsecond=0)

start_date = mytz.localize(start_date)
end_date   = mytz.localize(end_date)

events = []
for cal in ical_events:
  events += recurring_ical_events.of(cal).between(start_date, end_date)

month = dict()

def process_event(event, recent_events, special_calendars, t_allday):
  time, summary, uid, cal_name = event

  recent_class = "recent" if uid in [e.get('uid') for e in recent_events] else ""

  labels = [cal['label'] for cal in special_calendars if cal['name'] == cal_name]
  label = labels[0] if labels else t_allday

  if summary[0] == '*':
    label = special_calendars[0]['label']
    summary = summary[2:]

  if time:
    timeday = '<div class="event ' + recent_class + ' ' + cal_name + '"><time>' + time + '</time><span class="summary">' + summary + '</span></div>'
    allday = ""
    add_count = 0
  else:
    timeday = ""
    allday = '<div class="event all-day ' + recent_class + ' ' + cal_name + '"><time>' + label + '</time><span class="summary">' + summary + '</span></div>'
    add_count = 1

  return timeday, allday, add_count

for event in events:

  if event.name != "VEVENT":
    continue

  cal_date = event.get('dtstart').dt
  event_end = event.get('dtend').dt
  cal_name = event.get('cal_name')
  uid = event.get('uid')
  event_date = datetime.combine(cal_date, datetime.min.time())
  last_modified = event.get('last-modified')

  if last_modified is not None:
    last_modified = last_modified.dt
  else:
    last_modified = event.get('created').dt

  if event_date.tzinfo is None:
    event_date = mytz.localize(event_date)
  if event_date >= start_date and event_date <= end_date:
    dayindex = int(event_date.strftime('%Y%m%d'))
    summary = str(event.get('summary'))

    # check for full day event
    delta = event.get('dtend').dt - cal_date
    if delta.days >= 1:
      for i in range(0, delta.days):
        append_event(dayindex + i, None, summary, uid, cal_name)
    else:
      localtime = cal_date.astimezone(mytz).strftime("%H:%M")
      end_time = event_end.astimezone(mytz).strftime("%H:%M")
      append_event(dayindex, localtime + ' - ' + end_time, summary, uid, cal_name)

# Get all events that have been modified in the last three days
three_days_ago = now - timedelta(hours=72)
recent_events = [event for event in events if event.get('last-modified') and event.get('last-modified').dt > three_days_ago]

# load template
template_file = open(sys.argv[2], "r")
template = template_file.read()
template = template.replace("${TODAY_DAY}",    today.strftime("%-d"))
template = template.replace("${TODAY_WEEKDAY}",today.strftime("%A"))
template = template.replace("${TODAY_MONTH}",  today.strftime("%B"))
template = template.replace("${TODAY_YEAR}",   today.strftime("%Y"))
template = template.replace("${UPDATED}",      today.strftime("%d %b %H:%M"))

## print the days of the week
for i in range(0, 7):
  day_of_week = start_date + timedelta(days=i)
  if day_of_week.date() == today.date():
    template = template.replace("${DAY" + str(i + 1) + "}", '<b class="today">' + day_of_week.strftime("%a") + '</b>')
  else:
    template = template.replace("${DAY" + str(i + 1) + "}", day_of_week.strftime("%a"))

# process current day
dic_idx = date_idx(today)
allday=""
timeday=""
classes="day"

if today.weekday() >= 5:
  classes += " weekend"


if dic_idx in month:
  for event in month[dic_idx]:
    timeday_event, allday_event, _ = process_event(event, recent_events, special_calendars, t_allday)
    timeday += timeday_event
    allday += allday_event
else:
  allday = t_nothing_planned

template = template.replace("${TODAY_FULL_DAY_EVENTS}", allday)
template = template.replace("${TODAY_EVENTS}", timeday)
template = template.replace("${CLASSES}", classes)

row = '''\
  <td class="{classes}">
    <div class="date">{curday}</div>
    {alldayHTML}
    {timeday}
  </td>'''
# loop 21 days
dayrow=""
loop_day = start_date
while loop_day <= end_date:
  classes = "day"
  if loop_day.weekday() >= 5:
    classes += " weekend"
  if loop_day.day == current_day:
    classes += " today"

  dic_idx = date_idx(loop_day)
  allday=""
  timeday=""
  count = 0
  if dic_idx in month:
    events = month[dic_idx]
    # Sort the events by time. Events without a time (all-day events) will be put at the end.
    events.sort(key=lambda event: event[0] if event[0] else '23:59')
    for event in events:
      timeday_event, allday_event, add_count = process_event(event, recent_events, special_calendars, t_allday)
      timeday += timeday_event
      allday += allday_event
      count += add_count

  alldayHTML = ""
  if count > 0:
    alldayHTML = '<div class="all-day-events">' + allday + '</div>'

  if loop_day == start_date + timedelta(weeks=1):
    dayrow+='\n</tr>\n<tr class="week">'
  if loop_day == start_date + timedelta(weeks=2):
    dayrow+='\n</tr>\n<tr class="week">'
  dayrow+=row.format(classes=classes, alldayHTML=alldayHTML, timeday=timeday, curday=loop_day.day)+"\n"

  loop_day += timedelta(days=1)

template = template.replace("${DAY_ROW}", dayrow)

output_file = open(sys.argv[3], "w")
output_file.write(template)
output_file.close()
