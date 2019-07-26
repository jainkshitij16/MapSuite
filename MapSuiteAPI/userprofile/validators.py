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
    #now = pytz.utc.normalize(now)
    value = pytz.utc.normalize(value)
    if value > now:
        raise exceptions.ValidationError(value) #Please make sure you do not enter a future date and/or time

def latitudevalidator(value):

    """
    A custom validator method that checks if the latitude entered is in the valid range
    :param value: the latitude value entered by the latitude field in the annotation model
    :return: if the value entered is outside the acceptable range, it raises a validation error
    """

    if -90.0000 > value < 90.0000:
        raise exceptions.ValidationError('The acceptable range of latitudes is +-90')

def longitudevalidator(value):

    """
    A custom validator method that checks if the longitude entered is in the valid range
    :param value: the longitude value entered by the longitude field in the annotation model
    :return: if the value entered is outside the acceptable range, it raises a validation error
    """

    if -180.0000 > value < 180.0000:
        raise exceptions.ValidationError('The acceptable range of longitude is +-180')