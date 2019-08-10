from .models import Annotation,Userprofile, User, Community
from .serializers import UserprofileSerializer, AnnotationSerializer, CommunitySerializer
from .decorators import validate_user_request_data, validate_annotation_request_data, \
    validate_community_request_data, validate_object_change_data, validate_join_community
from rest_framework.views import Response, status
from rest_framework import generics, permissions
from django.contrib.auth.decorators import login_required

# Create your views here.

#TODO: Add if cases when user_privacy does not matter(custom permissions, is owner and/or current user)
#TODO: Add suport for adding a file through the front end
#login_required(login_url=)

#______________POST ENDPOINTS_____________________________________

class RegisterUser(generics.CreateAPIView):

    """
    Creates a new user

    :request verb: POST
    :endpoint : http://localhost:8000/register_user
    :parameter : The class that is used to generate the viewsets
    :return : Status 201, the created userprofile object
    """

    @validate_user_request_data
    def post(self, request, *args, **kwargs):
        #TODO; Fix this as well
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
        user_bio = request.data.get('user_bio')
        user_privacy = request.data.get('user_privacy')

        new_userprofile=Userprofile()

        if None in (first_name, last_name):
            new_user = User.objects.create_user(
                username=username,
                password=password,
                email=email)
        else:
            new_user = User.objects.create_user(
                username=username,
                password=password,
                email=email,
                first_name=first_name,
                last_name=last_name)

        new_userprofile.user=new_user
        new_userprofile.user_privacy=user_privacy

        if user_bio is not None:
            new_userprofile.user_bio = user_bio

        new_userprofile.save()

        return Response(
            data= UserprofileSerializer(new_userprofile).data,
            status= status.HTTP_201_CREATED
        )

class JoinCommunity(generics.UpdateAPIView):

    """
    Class to support the join community functionality

    :request verb: PATCH
    :endpoint : http://localhost:8000/username/join_community
    :parameter: The class that is used to generate the viewsets
    """

    @validate_join_community
    def patch(self, request, *args, **kwargs):

        """
        Updates the userprofile to add the requested communities

        :param request: contains the community names to add
        :param args:
        :param kwargs:
        :return: the updated userprofile with the community names as requested
        """

        user_community=request.data.get('user_community')
        username=kwargs['username']


class LoginView(generics.CreateAPIView):

    """
    Class to support the login functionality into the application

    :request verb: POST
    :endpoint : http://localhost:8000/login
    :parameter: The class that is used to generate the viewsets
    """

    def post(self, request, *args, **kwargs):

        """
        Creates a new token upon successful authentication

        :param request: user info
        :param args:
        :param kwargs:
        :return: Created token and status 201
        """

        #TODO: Add JWT Support

class RegisterAnnotation(generics.CreateAPIView):

    """
    Creates a new annotation

    :request verb: POST
    :endpoint : http://localhost:8000/add_annotation
    :parameter : The class that is used to generate the viewsets
    return : Status 201, the created annotation
    """

    @validate_annotation_request_data
    def post(self, request, *args, **kwargs):

        """

        Create a new annotation

        :param request: annotation request data
        :param args:
        :param kwargs:
        :return: staus 201 and the created annotation
        """
        username= request.data.get('username')
        location_name= request.data.get('location_name')
        latitude= request.data.get('latitude')
        longitude= request.data.get('longitude')
        ann_text = request.data.get('ann_text')
        ann_date_time = request.data.get('ann_date_time')
        label = request.data.get('label')
        annotation_community = request.data.get('annotation_community')
        owner=Userprofile.objects.get(user__username__iexact=username)

        new_annotation=Annotation()

        new_annotation.owner=owner
        new_annotation.location_name=location_name
        new_annotation.latitude=latitude
        new_annotation.longitude=longitude

        if ann_text is not None:
            new_annotation.ann_text=ann_text

        if ann_date_time is not None:
            new_annotation.ann_date_time=ann_date_time

        if label is not None:
            new_annotation.label=label

        if annotation_community is not None:
            try:
                community=owner.user_community.get(community_name__exact=annotation_community)
            except:
                return Response(
                    data={
                        'Error':'It seems you are not part of the community that you are trying to post too'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            new_annotation.annotation_community=community

        new_annotation.save()
        return Response(
            data=AnnotationSerializer(new_annotation).data,
            status=status.HTTP_201_CREATED
        )

class RegisterCommunity(generics.CreateAPIView):

    """
    Creates a new community

    :request verb: POST
    :endpoint : http://localhost:8000/add_community
    :parameter : The class that is used to generate the viewsets
    :return : status 201, the created community
    """

    @validate_community_request_data
    def post(self, request, *args, **kwargs):

        """
        Creates a new community

        :param request: community name
        :param args:
        :param kwargs:
        :return: status 201 and the community created
        """
        community_name = request.data.get('community_name')
        return Response(
            data=CommunitySerializer(Community.objects.create(community_name=community_name)).data,
            status=status.HTTP_201_CREATED
        )

class ObjectChange(generics.RetrieveUpdateDestroyAPIView):

    """
    Adds the selected lists of communities to the userprofile

    :request verb: GET, PATCH, DELETE
    :endpoint : http://localhost:8000/model/join_communities/pk
    :parameter : The class that is used to generate the viewsets
    :return : status 201, the updated userprofile
    """

    serializer_class = Userprofile

    def get_queryset(self):

        """
        Method to get the selected object from the correct model objects
        :return: the object(through pk) of the desired model
        """

        pk=self.kwargs['pk']
        if self.kwargs['model'] == 'userprofile':
            return Userprofile.objects.get(pk=pk)

        else:
            return Annotation.objects.get(pk=pk)

    @validate_object_change_data
    def get(self, request, *args, **kwargs):

        """
        Overrides the default functionality to manage different models

        :param request: the request and
        :param args:
        :param kwargs:
        :return: Returns the retrieved object with the accurate view and status 200
        """

        model = kwargs['model']
        if model=='userprofile':
                userprofile = self.get_queryset()
                userprofile_serialize = UserprofileSerializer(userprofile)
                return Response({
                    'Userprofile':userprofile_serialize.data
                },
                    status=status.HTTP_200_OK)
        elif model=='annotation':
                annotation = self.get_queryset()
                annotation_serialize = AnnotationSerializer(annotation)
                return Response({
                    'Annotation':annotation_serialize.data
                },
                    status=status.HTTP_200_OK)

    @validate_object_change_data
    def patch(self, request, *args, **kwargs):

        """
        Verb that updates the required model with the the updates

        :param request: Contains the JSON object of what is to be updated with what
        :param args:
        :param kwargs:
        :return: The updated model with the status 2XX
        """

        #TODO: Finish this and test the function

    @validate_object_change_data
    def delete(self, request, *args, **kwargs):

        """
        Verb that makes the user inaccessible to any data that has stored, either of the user or other users
        however for annotations, deletes the annotation from the database, DOES NOT for userprofile

        :param request:
        :param args:
        :param kwargs:
        :return: the updated model with the required status
        """

        model=kwargs['model']
        pk=kwargs['pk']
        if model=='userprofile':
            userprofile = Userprofile.objects.get(pk=pk)
            userprofile.isdeleted = True
            userprofile.save()
            return Response(
                data=UserprofileSerializer(userprofile).data,
                status=status.HTTP_200_OK
            )

        elif model=='annotation':
            annotation = Annotation.objects.get(pk=pk)
            annotation.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


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
    #permission_class = admin only

    def get_queryset(self):

        """
        Filters the users with the same groupname, looks for the exact match
        :return: selected users
        """

        return Userprofile.objects.filter(user_community=self.kwargs['community'])

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
                                         owner__isdeleted=False,
                                         owner__user_privacy=False)

class getUserLabel(generics.ListAPIView):

    """
    Returns all the annotations marked as label by the user

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
                                         owner__isdeleted=False,
                                         owner__user_privacy=False)

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
                                         owner__isdeleted=False,
                                         owner__user_privacy=False)

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
                                         owner__isdeleted=False,
                                         owner__user_privacy=False)

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
                                          isdeleted=False,
                                          user_privacy=False)

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
                                         owner__isdeleted=False,
                                         owner__user_privacy=False)

class getAnnotationsofCommunity(generics.ListAPIView):

    """
    Returns all the annotations for the specified community

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

        return Annotation.objects.filter(owner__user_community=self.kwargs['community'],
                                         owner__isdeleted=False,)



