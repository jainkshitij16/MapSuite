from rest_framework.response import Response
from rest_framework.views import status

def validate_user_request_data(fn):
    def user_decorator(*args, **kwargs):

        username = args[0].request.data.get('username','')
        password = args[0].request.data.get('password','')
        email = args[0].request.data.get('email','')
        first_name = args[0].request.data.get('first_name','')
        last_name = args[0].request.data.get('last_name', '')

        if not username and not password and not email:
            return Response(

            )

    return user_decorator

def validate_profile_request_data(fn):
    def profile_decorator(*args, **kwargs):
        print("Do this")

    return profile_decorator


def validate_annotation_request_data(fn):
    def annotation_decorator(*args, **kwargs):
        print("Do this")

    return annotation_decorator
