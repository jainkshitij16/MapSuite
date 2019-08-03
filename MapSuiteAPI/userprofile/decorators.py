from rest_framework.response import Response
from rest_framework.views import status

def validate_user_request_data(fn):
    def user_decorator(*args, **kwargs):
        username = args[0].request.data.get('username')
        password = args[0].request.data.get('password')
        email = args[0].request.data.get('email')
        private = args[0].request.data.get('private')

        if None in (username, password, email, private):
            return Response(
                data= {
                    'Error':'Username, password, email and privacy settings are required'
                },
                status= status.HTTP_400_BAD_REQUEST
            )
        return fn(*args,**kwargs)
    return user_decorator


def validate_annotation_request_data(fn):
    def annotation_decorator(*args, **kwargs):
        username = args[0].request.data.get('username')
        location_name = args[0].request.data.get('location_name')
        latitude = args[0].request.data.get('latitude')
        longitude = args[0].request.data.get('longitude')

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
        return fn(*args,**kwargs)
    return annotation_decorator
