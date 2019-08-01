from django.db import models
from django.contrib.auth.models import User
from .validators import *
# Create your models here.

class Community(models.Model):

    """
    A class which represents the community groups

    Attributes:

    community_name : Char field, max length = 30 characters, unique in nature
        name of the community created by the user

    private_community : Boolean field, required (default False)
        whether the community of users is private or public
    """

    community_name = models.CharField(unique=True, max_length=30, help_text='The name of the community the users belong to')
    private_community = models.BooleanField(default=False)

    def __str__(self):
        return self.community_name

    class Meta:
        verbose_name_plural = 'communities'


class Userprofile(models.Model):

    """
    A class which represents the userprofile object

    Attributes:
        user: User object, foreign key with auth.model User object, maps a one to one relationship
            the user details and the credentials (first_name, last_name, email, username, password)

        user_bio: Character field, max_length = 150 words
            the user biography, a representation of what the user is all about

        community: Community Object, foreign key with community, maps a many to one relationship
            the user grouping field, used to classify various users

        private: Boolean field, Required (default False)
            User flag, used to identify if the user is okay sharing the annotations or not

        isdeleted: Boolean field, Required (default False)
            User flag, used to identify if the user has deleted account or not
    """

    user = models.OneToOneField(User, on_delete= models.CASCADE, related_name='userprofile', default='')
    user_bio = models.CharField(max_length=180, help_text='Let all the users know something interesting about yourself')
    community = models.ForeignKey(Community, on_delete=models.CASCADE, help_text='The community user belongs too', default='')
    private = models.BooleanField(default=False, help_text='Would you like your profile to be accessible by everyone?')
    isdeleted = models.BooleanField(blank=False, default=False, help_text='Admin field only')

    def __str__(self):
        if self.user.first_name != '':
            return self.user.first_name
        return self.user.username


class Story(models.Model):

    """
    A class which represents the annotation groups

    Attributes:

    story_name : Char field, max_length = 30 characters, unique in nature
        name of the story which holds all of the relevant annotations

    story_owner : Userprofile owner, foreign key object, maps a one to many relationship
        the user who has created the story

    private_story : taken from the settings of the story_owner field
        Whether the story is private or not
    """

    story_name = models.CharField(unique=True, max_length=30, help_text='The name of the story')
    story_owner = models.ForeignKey(Userprofile, on_delete=models.CASCADE, help_text='the owner of the story', default='')
    private_story = models.BooleanField(default=False, help_text='Is the story private or not')

    def __str__(self):
        return self.story_name

    class Meta:
        verbose_name_plural = 'stories'


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

        label : Char field, presents choices of the tags, max length = 20
            A tag to recogonize if this annotation is part of any tag_choice

    """

    #Represent the various labels the users could have
    TAG_CHOICES = (
        ('home', 'Home'),
        ('office', 'Office'),
        ('research', 'Research'),
        ('school','School'),
        ('attraction','Attraction'),
        ('custom', 'Custom'),
    )

    owner = models.ForeignKey(Userprofile, related_name='location_user', on_delete=models.CASCADE, help_text='The user this annotation belongs too')
    location_name = models.CharField(max_length=30, blank=False, default='location name', help_text='The name of the location of the annotation')
    latitude = models.DecimalField(decimal_places=4, max_digits=10, validators=[latitudevalidator], blank=False, default=49.2642, help_text='The latitude of the location up to 4 decimal places')
    longitude = models.DecimalField(decimal_places=4, max_digits=10, validators=[longitudevalidator], blank=False, default=123.2532, help_text='The longitude of the location up to 4 decimal places')
    ann_text = models.CharField(max_length=1200, help_text='The desired story you want to tell to all other users')
    ann_date_time = models.DateTimeField(blank=False, default=timezone.now, validators=[datevalidator], help_text='The date and time this annotation holds importance for you')
    ann_file = models.FileField(blank=True)
    label = models.CharField(choices=TAG_CHOICES, help_text='The tag to identify whether the annotation represents any category', max_length=20, blank=True)
    stories = models.ForeignKey(Story, on_delete=models.CASCADE, help_text='The annotations that are part of the story', default='')


    def __str__(self):
        if self.owner.user.first_name != '':
            return '{}-{}'.format(self.location_name, self.owner.user.first_name)
        return '{}-{}'.format(self.location_name, self.owner.user.username)







