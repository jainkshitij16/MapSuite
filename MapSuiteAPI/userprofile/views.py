from .models import Annotation,Userprofile, User, Community
from .serializers import UserprofileSerializer, AnnotationSerializer, UserSerializer, CommunitySerializer
from .decorators import validate_user_request_data, validate_annotation_request_data
from rest_framework.views import Response, status
from rest_framework import generics, permissions

# Create your views here.

#TODO: add if case cases for when the request user is the owner->should also return private annotations, otherwise not

"""
GET: all users : admin only : done
GET: all locations : admin only : done
GET: all annotations by user : authenticated only : done
GET: all users which annotated a location : authenticated only : done
GET: a single annotation by the user : authenticated only : done
GET: all homes marked by the user : authenticated only : done
GET: all users in the same category : authenticated only : done
GET: A single user : authenticated only : done
GET: all annotations posted according to the category : authenticated, within that cat :

COULD BE COMBINED ENDPOINTS

POST: Create a new user : everyone
POST: Create a new annotation : authenticated only
PATCH: Update the user : authenticated only, owner only
PATCH: Update the annotation : authenticated only, owner only
DELETE: delete the selected user : authenticated only, owner only
DELETE: delete the selected annotation : authenticated only , owner only
"""

#______________POST ENDPOINTS_____________________________________

class RegisterUser(generics.CreateAPIView):

    """
    Creates a new user

    :request verb: POST
    :endpoint : http://localhost:8000/user
    :parameter : The class that is used to generate the viewsets
    :return : Status 201
    """
    #TODO: Complete the password validation thingy
    @validate_user_request_data
    def post(self, request, *args, **kwargs):

        """
        Creates a new user

        :param request: A request sent with data
        :param args:
        :param kwargs:
        :return: staus 201 on success
        """
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        #TODO: Complete the userprofile sign up fields

        if first_name is not None and last_name is not None:
            new_user = User.objects.create_user(
                username=username,
                password=password,
                email=email,
                first_name=first_name,
                last_name=last_name
            )
        else:
            new_user = User.objects.create_user(
                username=username,
                password=password,
                email=email
            )
        return Response(
            data= UserSerializer(new_user).data,
            status= status.HTTP_201_CREATED
        )

class RegisterAnnotation(generics.CreateAPIView):

    """
    Creates a new annotation

    :request verb: POST
    :endpoint : http://localhost:8000/annotation
    :parameter : The class that is used to generate the viewsets
    return : Status 201
    """

    @validate_annotation_request_data
    def post(self, request, *args, **kwargs):
        print("Blah")

#_____________USER GET ENDPOINTS___________________________________

class getcomm(generics.ListAPIView):
    """
    Returns all the communities

    :request verb: GET
    :endpoint : http://localhost:8000/communities
    :parameter generics.ListAPIView : The class that is used to generate the viewsets
    :return : All of the communities in the database (Format: JSON)
    """

    model = Community
    serializer_class = CommunitySerializer
    queryset = Community.objects.all()

class getAllUsers(generics.ListCreateAPIView):

    """
    Returns all the userprofiles

    :request verb: GET
    :endpoint : http://localhost:8000/users
    :parameter generics.ListAPIView : The class that is used to generate the viewsets
    :return : All of the userprofiles in the database (Format: JSON)
    """

    model = Userprofile
    serializer_class = UserprofileSerializer
    queryset = Userprofile.objects.all()
    #permission_classes = (permissions.IsAdminUser)

class getAllUserswithCom(generics.ListAPIView):

    """
    Returns all of the user which have the same community

    :request verb: GET
    :endpoint : http://localhost:8000/usersgroup=<str:community>
    :parameter generics.ListAPIView : The class that is used to generate the viewsets
    :return : All of the users in the in the same community (Format: JSON)
    """

    serializer_class = UserprofileSerializer

    def get_queryset(self):

        """
        Filters the users with the same groupname, looks for the exact match
        :return: selected users
        """

        return Userprofile.objects.filter(community=self.kwargs['community'],
                                          isdeleted=False,
                                          private=False)

class RetreiveUser(generics.RetrieveAPIView):
    """
    Returns the selected user

    Temporary function to return a user
    """

    model = Userprofile
    serializer_class = UserprofileSerializer
    queryset = Userprofile.objects.all()

class getUserAnnotations(generics.ListAPIView):

    """
    Returns all the annotations posted by the user

    :request : GET
    :endpoint : http://localhost:8000/username=<username>/annotations
    :parameter : generics.ListAPIView : The class that is used to generate the viewsets
    :return : All of the annotations by the selected user (Format: JSON)
    """

    serializer_class = AnnotationSerializer

    def get_queryset(self):

        """
        Overrides the get_queryset method
        This view should return a list of all the locations for the current user, username is the exact match

        :return: list of locations by the request.user
        """

        #user = self.request.user Use this post persmissions
        return Annotation.objects.filter(owner__user__username=self.kwargs['username'],
                                         owner__isdeleted=False)

class getUserLabel(generics.ListAPIView):

    """
    Returns all the annotations marked as home by the user

    :request: GET
    :endpoint : http://localhost:8000/username=<username>/label=<str:label>
    :parameter : generics.ListAPIView : The class that is used to generate the viewsets
    :return : All of the annotations marked as <label> by the selected user (Format: JSON)
    """

    serializer_class = AnnotationSerializer

    def get_queryset(self):

        """
        Overrides the default get method to filter for user's home(s), username is the exact match
        :return: list of the annotations marked as users home
        """

        return Annotation.objects.filter(owner__user__username=self.kwargs['username'],
                                         label=self.kwargs['label'],
                                         owner__isdeleted=False)

class getSingleUserAnnotation(generics.ListAPIView):

    """
    Returns the requested annotation of the user by the location name keyword

    :request: GET
    :endpoint : http://localhost:8000/username=<username>/annotations=<keyword>
    :parameter : generics.ListAPIView : The class that is used to generate the viewsets
    :return : Selected annotation(s) of the annotations by the selected user (Format: JSON)
    """

    serializer_class = AnnotationSerializer

    def get_queryset(self):

        """
        Filter the annotations to find the annotation to contain the keyword for the selected keyword and the username
        username is the exact match, keyword is not case sensitive
        :return: Selected annotations in the queryset of the selected user
        """

        return Annotation.objects.filter(owner__user__username=self.kwargs['username'],
                                         location_name__icontains=self.kwargs['keyword'],
                                         owner__isdeleted=False)

#_______________ANNOTATION GET ENDPOINTS____________________________________

class getAllAnnotations(generics.ListCreateAPIView):

    """
    Returns all the annotations

    :request verb: GET
    :endpoint : http://localhost:8000/annotations
    :parameter generics.ListAPIView : The class that is used to generate the viewsets
    :return : All of the annotations in the database (Format: JSON)
    """

    model = Annotation
    serializer_class = AnnotationSerializer
    queryset = Annotation.objects.all()

class RetreiveAnnotation(generics.RetrieveAPIView):
    """
    Returns the selected annotation

    Temporary function to return a annotation
    """

    model = Annotation
    serializer_class = AnnotationSerializer
    queryset = Annotation.objects.all()

class getAnnotionfromKeyword(generics.ListAPIView):

    """
    Returns the requested annotations by the location name keyword

    :request: GET
    :endpoint : http://localhost:8000/annotations=<keyword>
    :parameter : generics.ListAPIView : The class that is used to generate the viewsets
    :return : Selected annotation(s) of the annotations (Format: JSON)
    """

    serializer_class = AnnotationSerializer

    def get_queryset(self):

        """
        Filter the annotations to find the annotations that contains the the keyword
        keyword is not case sensitive
        :return: Selected annotations
        """

        return Annotation.objects.filter(location_name__icontains=self.kwargs['keyword'],
                                         owner__isdeleted=False)

class getAnnotationUsers(generics.ListAPIView):

    """
    Returns all the users that have annotated the same location

    :request: GET
    :endpoint : http://localhost:8000/annotations=<keyword>/users
    :parameter : generics.ListAPIView : The class that is used to generate the viewsets
    :return : All the users that have marked the the same location in the annotation (Format: JSON)
    """

    serializer_class = UserprofileSerializer

    def get_queryset(self):

        """
        Filter the users to find the users that have marked the same location
        keyword is not case sensitive
        :return: selected users
        """

        return Userprofile.objects.filter(location_user__location_name__icontains=self.kwargs['keyword'],
                                          isdeleted=False)

class getAnnotationwithTextKeyword(generics.ListAPIView):

    """
    Retuns all the annotations where the keyword has been present in the annotation description

    :request: GET
    :endpoint : http://localhost:8000/annotations/search_text=<keyword>
    :parameter : generics.ListAPIView : The class that is used to generate the viewsets
    :return : All the annotations that have a hit from the keyword (Format: JSON)
    """

    serializer_class = AnnotationSerializer

    def get_queryset(self):

        """
        Filters the annotations to find the annotations where the text contains the keyword
        keyword is not case sensitive
        :return: selected annotations
        """

        return Annotation.objects.filter(ann_text__icontains=self.kwargs['keyword'],
                                         owner__isdeleted=False)

class getAnnotationsofCommunity(generics.ListAPIView):

    """
    Returns all the annotations for the specified community for members otherwise all public

    :request: GET
    :endpoint : http://localhost:8000/annotations/usergroup=<community>
    :parameter : generics.ListAPIView : The class that is used to generate the viewsets
    :return : All the annotations for members of the community and public annotations for non members
    """

    serializer_class = AnnotationSerializer

    def get_queryset(self):

        """
        Filters the annotations to find the annotations present in the selected community
        :return: selected annotations
        """

        return Annotation.objects.filter(owner__community=self.kwargs['community'],
                                         owner__isdeleted=False,
                                         annotation_privacy=False)




