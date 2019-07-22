from .models import Annotation,Userprofile
from .serializers import UserprofileSerializer, AnnotationSerializer, GetallAnnotationsbyUserSerializer
# from rest_framework.views import Response, status
from rest_framework import generics

# Create your views here.

"""
GET: all users : admin only
GET: all locations : admin only
GET: all annotations by user : authenticated only
GET: all users which annotated a location : authenticated only
GET: a single annotation by the user : authenticated only

COULD BE COMBINED ENDPOINTS

POST: Create a new user : everyone
POST: Create a new annotation : authenticated only
PATCH: Update the user : authenticated only
PATCH: Update the annotation : authenticated only
DELETE: delete the selected user : authenticated only
DELETE: delete the selected annotation : authenticated only 
"""

class AllUsers(generics.ListCreateAPIView):

    """
    Returns all the userprofiles

    :request verb: GET, POST
    :endpoint : http://localhost:8000/users
    :parameter generics.ListAPIView : The class that is used to generate the viewsets
    :return : All of the userprofiles in the database (Format: JSON)
    """

    model = Userprofile
    serializer_class = UserprofileSerializer
    queryset = Userprofile.objects.all()

class AllAnnotations(generics.ListCreateAPIView):

    """
    Returns all the annotations

    :request verb: GET, POST
    :endpoint : http://localhost:8000/annotations
    :parameter generics.ListAPIView : The class that is used to generate the viewsets
    :return : All of the users in the database (Format: JSON)
    """

    model = Annotation
    serializer_class = AnnotationSerializer
    queryset = Annotation.objects.all()


class UserwithAnnotations(generics.ListCreateAPIView):

    """
    Returns all the annotations posted by the user

    :request : GET
    :endpoint : http://localhost:8000/user=<username>/annotations
    :parameter : generics.ListAPIView : The class that is used to generate the viewsets
    :return : All of the annotations by the selected user (Format: JSON)
    """
    model = Userprofile, Annotation
    serializer_class = GetallAnnotationsbyUserSerializer
    queryset = Annotation.objects.filter()


