import sys
from mplcal import MplCalendar

print("Reading", sys.argv[1])

calplot = MplCalendar(2020, 10)

#.add_event(1, 'a full day event')
#.add_event(1, 'HH:MM event capture')
#.color_day(14, 'mistyrose')

calplot.save("calplot.png", 15, 11.32, 100)

