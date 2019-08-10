from .models import Userprofile, Annotation, User, Community
from rest_framework import serializers


class CommunitySerializer(serializers.ModelSerializer):

    """
    A class which is used to represent the serializers for the Community object
    Required for transforming data from JSON to native python data types and vice-versa
    Contains similar fields with similar properties as the community object found in userprofile.models
    """

    class Meta:
        model = Community
        fields = ('community_name',)

class UserprofileSerializer(serializers.ModelSerializer):

    """
    A class which is used to represent the serializers for the Userprofile object
    Required for transforming data from JSON to native python data types and vice-versa
    Contains similar fields with similar properties as the Userprofile object found in userprofile.models
    """

    first_name = serializers.ReadOnlyField(source='user.first_name')
    last_name = serializers.ReadOnlyField(source='user.last_name')
    email = serializers.ReadOnlyField(source='user.email')
    username = serializers.ReadOnlyField(source='user.username')
    community = CommunitySerializer(source='user_community',many=True)


    class Meta:
        model = Userprofile
        fields = ('first_name',
                  'last_name',
                  'email',
                  'username',
                  'user_bio',
                  'community',
                  'user_privacy',)

class UserSerializer(serializers.ModelSerializer):

    """
    A class which is used to represent the serializers for the User object
    Required for transforming data from JSON to native python data types and vice-versa
    Contains similar fields with similar properties as the user object found in auth.user
    """

    class Meta:
        model = User
        fields = ('username',
                  'password',
                  'email',
                  'first_name',
                  'last_name')

class AnnotationSerializer(serializers.ModelSerializer):

    """
    A class which is used to represent the serializers for the Annotation object
    Required for transforming data from JSON to native python data types and vice-versa
    Contains similar fields with similar properties as the Annotation object found in userprofile.models
    """

    username = serializers.ReadOnlyField(source='owner.user.username')
    community = serializers.ReadOnlyField(source='annotation_community.community_name')

    class Meta:
        model = Annotation
        fields = ('username',
                  'location_name',
                  'latitude',
                  'longitude',
                  'ann_text',
                  'ann_date_time',
                  'label',
                  'ann_file',
                  'community')
