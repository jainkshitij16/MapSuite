from django.db import models
from django.contrib.auth.models import User
from .validators import latitudevalidator, longitudevalidator, datevalidator, timezone
# Create your models here.

class Community(models.Model):

    """
    A class which represents the community object

    Attributes:
        community_name : Character field, max_length : 50
    """

    community_name = models.CharField(max_length=50,unique=True, null=True, help_text='The name of the community needs to be unique')

    def __str__(self):
        return self.community_name

    class Meta:
        verbose_name_plural= 'communities'

class Userprofile(models.Model):

    """
    A class which represents the userprofile object

    Attributes:
        user: User object, foreign key with auth.model User object, maps a one to one relationship
            the user details and the credentials (first_name, last_name, email, username, password)

        user_bio: Character field, max_length = 180
            the user biography, a representation of what the user is all about

        user_community: Character field, max_length = 50
            the user grouping field, used to classify various users

        user_privacy: Boolean field, Required (default False)
            User flag, used to identify if the user is okay sharing the annotations or not

        isdeleted: Boolean field, Required (default False)
            User flag, used to identify if the user has deleted account or not
    """

    user = models.OneToOneField(User, on_delete= models.CASCADE, related_name='userprofile', default='')
    user_bio = models.CharField(max_length=180, help_text='Let all the users know something interesting about yourself')
    user_community = models.ManyToManyField(Community, blank=True)
    user_privacy = models.BooleanField(default=False, help_text='Would you like your profile to be accessible by everyone?')
    isdeleted = models.BooleanField(blank=False, default=False, help_text='Admin field only')

    def __str__(self):
        if self.user.first_name != '':
            return self.user.first_name
        return self.user.username

class Annotation(models.Model):

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

        ann_text : Character field, max_length = 1200
            the desired annotation in the text format on the point of interest

        ann_file : file field, yet to the implemented
            the desired annotation in the photo or the video format on the point of the interest

        ann_date_time : datetime field, required (default time.now)
            the date and/or time when the annotation was selected to be placed

        label : Text field, max_length = 10
            assigns a tag to the annotation

        community_annotation : Community Object, classify if the annotation belongs to the community, many to many
            the annotation grouping field, used to classify various annotations

        story_privacy : Boolean field, Required (default False)
            user flag, used to identify the privacy settings of the stories

    """

    owner = models.ForeignKey(Userprofile, related_name='location_user', on_delete=models.CASCADE, help_text='The user this annotation belongs too')
    location_name = models.CharField(max_length=30, blank=False, default='location name', help_text='The name of the location of the annotation')
    latitude = models.DecimalField(decimal_places=4, max_digits=10, validators=[latitudevalidator], blank=False, default=49.2642, help_text='The latitude of the location up to 4 decimal places')
    longitude = models.DecimalField(decimal_places=4, max_digits=10, validators=[longitudevalidator], blank=False, default=123.2532, help_text='The longitude of the location up to 4 decimal places')
    ann_text = models.CharField(max_length=1200, help_text='The desired story you want to tell to all other users')
    ann_date_time = models.DateTimeField(blank=False, default=timezone.now, validators=[datevalidator], help_text='The date and time this annotation holds importance for you')
    ann_file = models.FileField(blank=True)
    label = models.TextField(help_text='The tag to identify whether the annotation represents any category', blank=True)
    annotation_community = models.ForeignKey(Community, blank=True, on_delete=models.CASCADE, null=True)



    def __str__(self):
        if self.owner.user.first_name != '':
            return '{}-{}'.format(self.location_name, self.owner.user.first_name)
        return '{}-{}'.format(self.location_name, self.owner.user.username)






