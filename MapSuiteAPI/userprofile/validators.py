from django.core import exceptions
from django.utils import timezone
import pytz


def datevalidator(value):

    """
    A custom validator method that checks if the date of the annotation is not set in the future
    :param value: the date set by the field ann_date_time (date and time entered by the user for posting the pin)
    :return: if the date is set in the future, raises a validation error
    """
    now = timezone.datetime.now()
    now = pytz.utc.localize(now)
    if value > now:
        raise exceptions.ValidationError('Annotation cannot be from a future date')