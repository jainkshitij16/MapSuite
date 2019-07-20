from .models import Userprofile, Location
from rest_framework import serializers

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

    class Meta:
        model = Userprofile
        fields = ('first_name',
                  'last_name',
                  'email',
                  'username',
                  'bio')

class LocationSerializer(serializers.ModelSerializer):

    """
    A class which is used to represent the serializers for the Location object
    Required for transforming data from JSON to native python data types and vice-versa
    Contains similar fields with similar properties as the Location object found in userprofile.models
    """

    first_name = serializers.ReadOnlyField(source='owner.user.first_name')
    last_name = serializers.ReadOnlyField(source='owner.user.last_name')
    username = serializers.ReadOnlyField(source='owner.user.username')

    class Meta:
        model = Location
        fields = ('username',
                  'location_name',
                  'latitude',
                  'longitude',
                  'ann_text',
                  'ann_date_time')