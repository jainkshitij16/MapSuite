from rest_framework.response import Response
from rest_framework.views import status
from django.contrib.auth.password_validation import validate_password, password_validators_help_texts
from django.core.validators import validate_email
from .models import User
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
        return fn(*args,**kwargs)
    return user_decorator


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
        return fn(*args,**kwargs)
    return annotation_decorator

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
        return fn(*args,**kwargs)
    return community_decorator