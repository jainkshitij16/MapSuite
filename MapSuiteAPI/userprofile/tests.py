from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from .models import Userprofile, Annotation, User
from .serializers import UserprofileSerializer, AnnotationSerializer
from rest_framework.views import status
from django.utils import timezone


# Create your tests here.

class UserTestClass(APITestCase):
    client = APIClient()

    @staticmethod
    def createUser(username='', password=''):
        if username !='' and password !='':
            return User.objects.create(username=username,
                                       password=password)

    @staticmethod
    def createUserProfile(user= User, user_bio=''):
        if user is not None and user_bio !='':
            return Userprofile.objects.create(user=user,
                                              user_bio=user_bio)

    @staticmethod
    def createAnnotation(owner=Userprofile, location_name='', latitude=-1, longitude=-1, ann_text='', ann_date_time=''):
        if owner is not None and location_name != '' and latitude !=-1 and longitude !=-1 and ann_text !='' and ann_date_time is not None:
            return Annotation.objects.create(owner=owner,
                                             location_name=location_name,
                                             latitude=latitude,
                                             longitude=longitude,
                                             ann_text=ann_text,
                                             ann_date_time=ann_date_time)
    @classmethod
    def setUpTestData(cls):
       # cls.user = User.objects.create_superuser(username )


