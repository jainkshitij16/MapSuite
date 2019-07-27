from .models import Annotation,Userprofile
from .serializers import UserprofileSerializer, AnnotationSerializer
from rest_framework.views import Response, status
from rest_framework import generics

# Create your views here.

"""
GET: all users : admin only : done
GET: all locations : admin only : done
GET: all annotations by user : authenticated only : done
GET: all users which annotated a location : authenticated only
GET: a single annotation by the user : authenticated only
GET: all homes marked by the user : authenticated only : done
GET: all users in the same category : authenticated only
GET: A single user : authenticated only : done

COULD BE COMBINED ENDPOINTS

POST: Create a new user : everyone
POST: Create a new annotation : authenticated only
PATCH: Update the user : authenticated only
PATCH: Update the annotation : authenticated only
DELETE: delete the selected user : authenticated only
DELETE: delete the selected annotation : authenticated only 
"""

class getAllUsers(generics.ListCreateAPIView):

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

class getAllAnnotations(generics.ListCreateAPIView):

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

    # Change get queryset

class RetreiveUser(generics.RetrieveAPIView):
    """
    Returns the selected user

    Temporary function to return a user
    """

    model = Userprofile
    serializer_class = UserprofileSerializer
    queryset = Userprofile.objects.all()


class RetreiveAnnotation(generics.RetrieveAPIView):
    """
    Returns the selected annotation

    Temporary function to return a annotation
    """

    model = Annotation
    serializer_class = AnnotationSerializer
    queryset = Annotation.objects.all()



class getUserAnnotations(generics.ListCreateAPIView):

    """
    Returns all the annotations posted by the user

    :request : GET
    :endpoint : http://localhost:8000/username=<username>/annotations
    :parameter : generics.ListCreateAPIView : The class that is used to generate the viewsets
    :return : All of the annotations by the selected user (Format: JSON)
    """

    serializer_class = AnnotationSerializer

    def get_queryset(self):

        """
        Overrides the get_queryset method
        This view should return a list of all the locations for the current user

        :return: list of locations by the request.user
        """

        #user = self.request.user Use this post persmissions
        return Annotation.objects.filter(owner__user__username=self.kwargs['username'])

    # def get(self, request, *args, **kwargs):
    #     """
    #     Overrides the default get method
    #
    #     :param request:
    #     :param args:
    #     :param kwargs:
    #     :return: a view with the returned queryset items
    #     """
    #
    #     try:
    #         userprofiles = Userprofile.objects.filter(user__username=self.kwargs['username'])
    #         annotations = self.get_queryset()
    #
    #         userprofiles_serializer = UserprofileSerializer(userprofiles, many=True)
    #         annotations_serializer = AnnotationSerializer(annotations, many=True)
    #
    #         return Response({
    #             'userprofile': userprofiles_serializer.data,
    #             'user_annotations' : annotations_serializer.data
    #         })
    #
    #     except:
    #         return Response(status.HTTP_404_NOT_FOUND)

class getUserHomes(generics.ListCreateAPIView):

    """
    Returns all the annotations marked as home by the user

    :request: GET
    :endpoint : http://localhost:8000/username=<username>/annotations/home
    :parameter : generics.ListCreateAPIView : The class that is used to generate the viewsets
    :return : All of the annotations by the selected user (Format: JSON)
    """

    serializer_class = AnnotationSerializer

    def get_queryset(self):

        """
        Overrides the default get method to filter for user's home(s)
        :return: list of the annotations marked as users home
        """

        return Annotation.objects.filter(owner__user__username=self.kwargs['username'], ishome=True)




