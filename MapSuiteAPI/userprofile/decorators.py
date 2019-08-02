from rest_framework.response import Response
from rest_framework.views import status

def validate_user_request_data(fn):
    def user_decorator(*args, **kwargs):

        username = args[0].request.data.get('username','')
        password = args[0].request.data.get('password','')
        email = args[0].request.data.get('email','')

        if not username and not password and not email:
            return Response(
                data= {
                    'Error' : 'Username, password and email are required'
                },
                status= status.HTTP_400_BAD_REQUEST
            )
        return fn(*args,**kwargs)
    return user_decorator

def validate_profile_request_data(fn):
    def profile_decorator(*args, **kwargs):
        print("Do this")

    return profile_decorator


def validate_annotation_request_data(fn):
    def annotation_decorator(*args, **kwargs):
        print("Do this")

    return annotation_decorator
