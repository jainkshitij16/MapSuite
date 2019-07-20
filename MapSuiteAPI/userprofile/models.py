from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class Userprofile(models.Model):

    """
    A class which represents the userprofile object

    Attributes:
        user: User object, foreign key with auth.model User object, maps a one to one relationship
            the user details and the credentials (first_name, last_name, email, username, password)

        user_bio: Character object, max_length = 150 words
            the user biography, a representation of what the user is all about
    """

    user = models.OneToOneField(User, on_delete= models.CASCADE, related_name='userprofile', default='')
    user_bio = models.CharField(max_length=180)

    def __str__(self):
        if self.user.first_name != '':
            return self.user.first_name
        return self.user.username




class Location(models.Model):

    """
    A class with represents the locaion object

    Attributes:

        owner: Userprofile object, foreign key with userprofile object, maps a many to one relationship
            the userprofile object and the details of the users

        location_name: Character field, required (default location name)
            the location name of the location to annotate

        latitude: Decimal field, decimal places = 4, max_digits = 10, required (default 49.2642)
            the latitude of the location marked

        longitude: Decimal field, decimal places = 4, max_digits = 10, required (default 123.2532)
            the longitude of the location marked

        ann_text : Character field
            the desired annotation in the text format on the point of interest

        ann_file : file field, yet to the implemented
            the desired annotation in the photo or the video format on the point of the interest

        ann_date_time : datetime field, required (default time.now)
            the date and/or time when the annotation was selected to be placed
    """

    owner = models.ForeignKey(Userprofile, related_name='location_user', on_delete=models.CASCADE)
    location_name = models.CharField(max_length=30, blank=False, default='location name')
    latitude = models.DecimalField(decimal_places=4, max_digits=10, blank=False, default=49.2642)
    longitude = models.DecimalField(decimal_places=4, max_digits=10, blank=False, default=123.2532)
    ann_text = models.CharField(max_length=250)
    ann_date_time = models.DateTimeField(blank=False, default=timezone.now)

    def __str__(self):
        if self.owner.user.first_name != '':
            return '{}-{}'.format(self.location_name, self.owner.user.first_name)
        return '{}-{}'.format(self.location_name, self.owner.user.username)