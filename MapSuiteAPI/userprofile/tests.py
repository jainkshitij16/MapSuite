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
    def createUserProfile(user= User, user_bio='', private=False , isdeleted=False):
        if user is not None and user_bio !='' and isdeleted is not None and private is not None:
            return Userprofile.objects.create(user=user,
                                              user_bio=user_bio,
                                              private=private,
                                              isdeleted=isdeleted)

    @staticmethod
    def createAnnotation(owner=Userprofile,
                         location_name='',
                         latitude=-1.00,
                         longitude=-1.00,
                         ann_text='',
                         ann_date_time='',
                         label='home',
                         annotation_privacy=False):
        if owner is not None and location_name != '' and latitude !=-1 and longitude !=-1 and ann_text !='' and ann_date_time is not None:
            return Annotation.objects.create(owner=owner,
                                             location_name=location_name,
                                             latitude=latitude,
                                             longitude=longitude,
                                             ann_text=ann_text,
                                             ann_date_time=ann_date_time,
                                             label=label,
                                             annotation_privacy=annotation_privacy)
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_superuser(username='test',
                                                 password='mapsuite',
                                                 email='test@mapsuite.tech')

        user_one = cls.createUser(username='random', password='user1')
        user_two = cls.createUser(username='random2', password='user2')
        user_three = cls.createUser(username='random3', password='user3')
        user_four = cls.createUser(username='random4', password='user4')
        user_five = cls.createUser(username='random5', password='user5')
        user_six = cls.createUser(username='random6', password='user6')

        userprofile_one = cls.createUserProfile(user=user_one,
                                                user_bio='Test case number one',
                                                private=True,
                                                isdeleted=False)

        userprofile_two = cls.createUserProfile(user=user_two,
                                                user_bio='Test case number two',
                                                private=False,
                                                isdeleted=False)

        userprofile_three = cls.createUserProfile(user=user_three,
                                                  user_bio='Test case number three',
                                                  private=True,
                                                  isdeleted=False)

        userprofile_four = cls.createUserProfile(user=user_four,
                                                 user_bio='Test case number four',
                                                 private=False,
                                                 isdeleted=False)

        userprofile_five = cls.createUserProfile(user=user_five,
                                                 user_bio='Test case number five',
                                                 private=True,
                                                 isdeleted=False)

        userprofile_six = cls.createUserProfile(user=user_six,
                                                user_bio='Test case number six',
                                                private=False,
                                                isdeleted=False)

        cls.createAnnotation(owner=userprofile_one,
                             location_name='Test user location number 1',
                             latitude=88.1234,
                             longitude=122.4356,
                             ann_text='Test user ann text number 1',
                             ann_date_time=timezone.now(),
                             label='Custom',
                             annotation_privacy=False)

        cls.createAnnotation(owner=userprofile_two,
                             location_name='Test user location number 2',
                             latitude=55.3452,
                             longitude=97.2432,
                             ann_text='Test user ann text number 2',
                             ann_date_time=timezone.now(),
                             label='Home',
                             annotation_privacy=True)

        cls.createAnnotation(owner=userprofile_three,
                             location_name='Test user location number 3',
                             latitude=34.3452,
                             longitude=175.2432,
                             ann_text='Test user ann text number 3',
                             ann_date_time=timezone.now(),
                             label='Office',
                             annotation_privacy=False)

        cls.createAnnotation(owner=userprofile_four,
                             location_name='UBC',
                             latitude=43.5434,
                             longitude=122.4534,
                             ann_text='Test user ann text number 4',
                             ann_date_time=timezone.now(),
                             label='Research',
                             annotation_privacy=False)

        cls.createAnnotation(owner=userprofile_five,
                             location_name='Test',
                             latitude=22.3454,
                             longitude=120.4356,
                             ann_text='Test user ann text number 5',
                             ann_date_time=timezone.now(),
                             label='Attraction',
                             annotation_privacy=False)

        cls.createAnnotation(owner=userprofile_six,
                             location_name='UBC',
                             latitude=45.1243,
                             longitude=123.5678,
                             ann_text='Test user ann text number 4',
                             ann_date_time=timezone.now(),
                             label='Home',
                             annotation_privacy=False)

    def test_GetAllUsers(self):

        """
        The test is to check GET request at the endpoint: http://localhost:8000/users
        :return: all the users that currently present in the database
        """
        response = self.client.get(reverse('all-users'))
        expected = Userprofile.objects.all()
        serialized = UserprofileSerializer(expected, many=True)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_GetAllAnnotations(self):

        """
        The test is to check the GET request at the endpoint: http://localhost:8000/annotations
        :return: all the annotations currently present in the database
        """

        response = self.client.get(reverse('all-annotations'))
        expected = Annotation.objects.all()
        serialized = AnnotationSerializer(expected, many=True)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def findUser(self, pk=0):

        """
        Helper function for test_GetOneUser to call the endpoint using the kwargs
        :param pk: the primary key given by the url
        :return: returns the serialized user object
        """

        return self.client.get(reverse('one-user', kwargs={
            'pk':pk}))

    def test_GetOneUser(self):

        """
        The test is to check the GET request at the endpoint: http://localhost:8000/users/<pk>
        :return: the selected user according to the primary key passed
        """

        response = self.findUser(pk=3)
        expected = Userprofile.objects.get(user_bio='Test case number three')
        serialized = UserprofileSerializer(expected)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def findAnnotation(self, pk=0):

        """
        Helper function for test_GetOneAnnotation to call the endpoint using the kwargs
        :param pk: the primary key given by the url
        :return: returns the serialized annotation object
        """

        return self.client.get(reverse('one-annotation', kwargs={
            'pk':pk}))

    def test_GetOneAnnotation(self):

        """
        The test is to check the GET request at the endpoint: http://localhost:8000/annotations/<pk>
        :return: the selected annotation according to the primary key passed
        """

        response = self.findAnnotation(pk=2)
        expected = Annotation.objects.get(ann_text='Test user ann text number 2')
        serialized = AnnotationSerializer(expected)
        self.assertEquals(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)