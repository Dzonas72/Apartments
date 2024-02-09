from calendar import HTMLCalendar
from .models import Event, Room


class Calendar(HTMLCalendar):

    def __init__(self, year=None, month=None):
        self.year = year
        self.month = month
        super(Calendar, self).__init__()


    def formatday(self, day, events, room_id=None):
        if not room_id:
            events_per_day = events.filter(start_time__day__lte=day, end_time__day__gt=day)
        else:
            room = Room.objects.get(pk=room_id)
            events_per_day = events.filter(start_time__day__gt=day, room=room)
        d = ''
        for event in events_per_day:
            d += f'<li style=text-color:red> {event.get_html_url} </li>'
        if day != 0:
            if not events_per_day:
                return f"<td><span class='date'>{day}</span><ul> {d} </ul></td>"
            return f"<td style=background-color:yellow><span class='date'><a href='/apartment/room_availability'>{day}</a></span><ul>{d}</ul></td>"
        for event in events_per_day:
            d += f'<li> {event.get_html_url} </li>'
        return '<td></td>'


    def formatweek(self, theweek, events):
        week = ''
        for d, weekday in theweek:
            week += self.formatday(d, events)
        return f'<tr>{week}</tr>'


    def formatmonth(self, withyear=True, events=None):
        events = Event.objects.filter(start_time__year=self.year, start_time__month=self.month)
        print(events)
        cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
        cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week, events)}\n'
        return cal
