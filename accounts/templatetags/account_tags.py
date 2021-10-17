from django import template
from django.utils import timezone

import pytz

register = template.Library()


@register.simple_tag
def time_now(tz_name: str, dt_format: str='%B %d, %Y %R'):
    """
    Custom template tag to return the current date and time for a timezone in the specified
    date format

    in the template, the timezone name is retrieved from the query parameter (?tz=<timezone name>)
    """
    now = timezone.now() # gives utc time by default
    if tz_name and tz_name.lower() != 'utc':
        try:
            tz = pytz.timezone(zone=tz_name)
            now = now.astimezone(tz=tz)
        except pytz.exceptions.UnknownTimeZoneError:
            pass
        
    return now.strftime(dt_format)
