from rest_framework.response import Response
from rest_framework.views import status
from django.contrib.auth.password_validation import validate_password, password_validators_help_texts
from django.core.validators import validate_email
from .models import User, Annotation, Userprofile, Community
from .validators import latitudevalidator, longitudevalidator

def validate_user_request_data(fn):
    def user_decorator(*args, **kwargs):
        username= args[0].request.data.get('username')
        password= args[0].request.data.get('password')
        email= args[0].request.data.get('email')
        user_privacy= args[0].request.data.get('user_privacy')

        if None in (username, password, email, user_privacy):
            return Response(
                data= {
                    'Error':'Username, password, email and privacy settings are required'
                },
                status= status.HTTP_400_BAD_REQUEST
            )
        try:
            validate_email(email)
        except:
            return Response(
                data={
                    'Error': 'Please enter a valid email'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            validate_password(password,user=User(username=username,
                                                 email=email))
        except:
            return Response(
                data={
                    'Error': password_validators_help_texts()
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        if User.objects.filter(username=username):
            return Response(data={
                'Error':'The username already exists, please use a different username'
            },
                status=status.HTTP_400_BAD_REQUEST
            )
        return fn(*args,**kwargs)
    return user_decorator

def validate_user_login_data(fn):
    def login_decorator(*args, **kwargs):
        username= args[0].request.data.get('username')
        password= args[0].request.data.get('password')

        if None in (username, password):
            return Response(
                data= {
                    'Error':'Username, password'
                },
                status= status.HTTP_400_BAD_REQUEST
            )
        try:
            user = Userprofile.objects.get(user__username=username)
        except:
            return Response(
                data={
                    'Error': 'The user with the desired credentials does not exist'
                },
                status= status.HTTP_400_BAD_REQUEST
            )
        if user.isdeleted:
            return Response(data={
                'Error': 'The user with the desired credentials does not exists or has been deleted'
            },
            status= status.HTTP_400_BAD_REQUEST
            )
        return fn(*args,**kwargs)
    return login_decorator


def validate_annotation_request_data(fn):
    def annotation_decorator(*args, **kwargs):
        username= args[0].request.data.get('username')
        location_name= args[0].request.data.get('location_name')
        latitude= args[0].request.data.get('latitude')
        longitude= args[0].request.data.get('longitude')

        if username is None:
            return Response(
                data={
                    'Error':'Bad Frontend Development, username should automatically come from request.owner.username'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        if None in (location_name,latitude,longitude):
            return Response(
                data={
                    'Error':'Please make sure the values of location name, latitude and longitude are entered correctly'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            longitudevalidator(float(longitude))
        except:
            return Response(
                data={
                    'Error': 'The acceptable range of longitude is +-180'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            latitudevalidator(float(latitude))
        except:
            return Response(
                data={
                    'Error': 'The acceptable range of latitude is +-90'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            Userprofile.objects.get(user__username__iexact=username)
        except:
            return Response(
                data={
                    'Error':'The username does not exist, Please make sure you enter a valid username'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        return fn(*args,**kwargs)
    return annotation_decorator

def validate_annotation_file(fn):
    def file_decorator(*args, **kwargs):
        pk=kwargs['pk']
        file=args[0].request.FILES['file']

        if pk is None:
            return Response(
                data={
                    'Error': 'Something went wrong with id of the annotation'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            Annotation.objects.get(pk=pk)
        except:
            return Response(
                data={
                    'Error':'Something went wrong with the annotation id getter'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        if file is None:
            return Response(
                data={
                    'Error': 'The file is not present'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        return fn(*args, **kwargs)
    return file_decorator

def validate_community_request_data(fn):
    def community_decorator(*args, **kwargs):
        community_name= args[0].request.data.get('community_name')

        if community_name is None:
            return Response(
                data={
                    'Error': 'Please enter the community name'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        elif community_name=='':
            return Response(
                data={
                    'Error': 'The community name cannot be blank'
            },
            status=status.HTTP_400_BAD_REQUEST
            )
        if Community.objects.filter(community_name=community_name):
            return Response(
                data={
                    'Error':'the community already exists, please enter through join community'
                },
            status=status.HTTP_400_BAD_REQUEST
            )
        return fn(*args,**kwargs)
    return community_decorator

def validate_object_change_data(fn):
    def object_decorator(*args, **kwargs):

        model=kwargs['model']
        pk=kwargs['pk']

        if model=='userprofile':
            try:
                Userprofile.objects.get(pk=pk)
            except:
                return Response(data={
                    'Error':'Could not find the desired user, are you sure you are looking for the right user profile'
                },
                    status=status.HTTP_400_BAD_REQUEST)
        elif model=='annotation':
            try:
                Annotation.objects.get(pk=pk)
            except:
                return Response(data={
                    'Error':'Could not find the desired annotation, are you sure you are looking for the right annotation'
                },
                    status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data={
                'Error': 'Please make sure the request arguments are correct'
            },
                status=status.HTTP_400_BAD_REQUEST)
        return fn(*args, **kwargs)
    return object_decorator

def validate_join_community(fn):
    def join_decorator(*args, **kwargs):

        user_community=args[0].request.data.get('user_community')
        username=kwargs['username']

        if None in (user_community, username):
            return Response(
                data={
                    'Error': 'Please enter the community name and username'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        elif user_community=='':
            return Response(
                data={
                    'Error': 'The community name cannot be blank'
            },
            status=status.HTTP_400_BAD_REQUEST
            )

        try:
            Userprofile.objects.get(user__username__exact=username)
        except:
            return Response(data={
                'Error':'Could not get the userprofile to add the community too'
            },
                status=status.HTTP_400_BAD_REQUEST
            )
        return fn(*args, **kwargs)
    return join_decorator

