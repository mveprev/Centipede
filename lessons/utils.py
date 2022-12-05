from datetime import datetime, timedelta
from calendar import HTMLCalendar
from .models import Schedule

'''Create a calendar'''
class Calendar(HTMLCalendar):
    def __init__(self, user, year=None, month=None):
        self.year = year
        self.month = month
        self.user = user
        super(Calendar, self).__init__()

    def formatday(self, day, schedules):
        events_per_day = schedules.filter(start_date__day=day).order_by('start_time')
        d = ''
        for event in events_per_day:
            d += f'<li>{event.start_time} {event.duration}min</li>'
        if day != 0:
            return f"<td><span class='date'>{day}</span><ul> {d} </ul></td>"
        return '<td></td>'

    def formatweek(self, theweek, events):
        week = ''
        for d, weekday in theweek:
            week += self.formatday(d, events)
        return f'<tr> {week} </tr>'

    def formatmonth(self, withyear=True):
        events = Schedule.objects.filter(start_date__year=self.year, start_date__month=self.month, teacher=self.user)

        cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
        cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week, events)}\n'
        return cal
