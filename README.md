# TeamRocket
Spring 2022 UNT Capstone, Team Rocket.

# Project: Meet Me Halfway
# Project Overview
#Members:
Cameron Smyrl
Matt Curtin
Kalvin Garcia
Logan Wheeler
Sometimes 2 people need to meet halfway (more or less) between where they are.  
Common examples are custody exchanges or trying to meet a relative/friend who is
passing through on a trip.  It should have features like noting any favorites, suggesting
nearby restaurants or police stations.  Users need to be able to enter their address and
the app gives them options on where to meet (that are near something – so not in the
middle of nowhere) based on their needs (e.g., at a police station).

dependencies:
  Kivy:
    `pip install kivy` <- also installs kivy-garden, I think.
  KivyMD (so far optional):
    `pip install kivymd`
  MapView:
    `pip install mapview`
    `garden install mapview` (optional)
  KivyCalendar:
    `pip install KivyCalendar` (needs modification to be compatible with Python v3.0+)

"Updating" KivyCalendar:
  here is a link to the guy who did it on stack overflow: https://stackoverflow.com/questions/48518358/getting-error-no-module-named-calendar-ui-even-though-kivycalendar-has-been

  Go here: KivyCalendar/__init__.py
    change `from calendar_ui import DatePicker, CalendarWidget`
    to `from .calendar_ui import DatePicker, CalendarWidget`

  Then go here: KivyCalendar/calendar_data.py
    change `from calendar import TimeEncoding, month_name, day_abbr, Calendar, monthrange`
    to `from calendar import month_name, day_abbr, Calendar, monthrange`

    add this:
    `
    import locale as _locale

    class TimeEncoding:
      def __init__(self, locale):
        self.locale = locale

      def __enter__(self):
        self.oldlocale = _locale.setlocale(_locale.LC_TIME, self.locale)
        return _locale.getlocale(_locale.LC_TIME)[1]

      def __exit__(self, *args):
        _locale.setlocale(_locale.LC_TIME, self.oldlocale)
      `

    Finally go here: KivyCalendar/calendar_ui.py
      change `import calendar_data as cal_data`
      to `from . import calendar_data as cal_data`

    You're done! Go on and prosper, the UI should run.
