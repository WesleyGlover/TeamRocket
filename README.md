# Project Team: TeamRocket
## Project Team Overview
### Members:
Cameron Smyrl   : smyrlcam<br />
Matt Curtin     : MattCurtin12<br />
Kalvin Garcia   : OchaKaru<br />
Logan Wheeler   : BraysonWheeler<br />
Wesley Glover   : WesleyGlover<br />

### Description:
Spring 2022 UNT Capstone, Team Rocket.

# Project: Meet Me Halfway
# Project Overview
#Members:
Cameron Smyrl
Matt Curtin
Kalvin Garcia
Logan Wheeler
Wesley Glover

Sometimes 2 people need to meet halfway (more or less) between where they are.  
Common examples are custody exchanges or trying to meet a relative/friend who is
passing through on a trip.  It should have features like noting any favorites, suggesting
nearby restaurants or police stations.  Users need to be able to enter their address and
the app gives them options on where to meet (that are near something – so not in the
middle of nowhere) based on their needs (e.g., at a police station).

## Dependencies:
  Kivy: <br />
    `pip install kivy` <- also installs kivy-garden, I think. <br />
  KivyMD (no longer optional): <br />
    `pip install kivymd` <br />
  Twisted: <br />
    `pip install twisted` <br />
  MapView: <br />
    `pip install mapview` <br />
    `garden install mapview` (optional) <br />
  KivyCalendar: <br />
    `pip install KivyCalendar` (needs modification to be compatible with Python v3.0+) <br />
  Geopy: <br />
    `pip install geopy` <br />
  Geocoder:<br />
    `pip install geocoder` <br />
  Py3-validate-email:<br />
    `pip install py3-validate-email` <br />
  MySQL:<br />
    `pip install mysql-connector-python` <br />
  Scipy:<br />
    `pip install scipy` <br />

"Updating" KivyCalendar: <br />
  here is a link to the guy who did it on stack overflow: https://stackoverflow.com/questions/48518358/getting-error-no-module-named-calendar-ui-even-though-kivycalendar-has-been

  Go here: KivyCalendar/__init__.py <br />
    change `from calendar_ui import DatePicker, CalendarWidget` <br />
    to `from .calendar_ui import DatePicker, CalendarWidget` <br />

  Then go here: KivyCalendar/calendar_data.py <br />
    change `from calendar import TimeEncoding, month_name, day_abbr, Calendar, monthrange` <br />
    to `from calendar import month_name, day_abbr, Calendar, monthrange` <br />
    add this: <br />

   ```python
    import locale as _locale

    class TimeEncoding:
      def __init__(self, locale):
        self.locale = locale

      def __enter__(self):
        self.oldlocale = _locale.setlocale(_locale.LC_TIME, self.locale)
        return _locale.getlocale(_locale.LC_TIME)[1]

      def __exit__(self, *args):
        _locale.setlocale(_locale.LC_TIME, self.oldlocale)
   ```
   Finally go here: KivyCalendar/calendar_ui.py <br />
      change `import calendar_data as cal_data` <br />
      to `from . import calendar_data as cal_data` <br />

   You're done! Go on and prosper, the UI should run.
