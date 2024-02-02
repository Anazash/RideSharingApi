from rest_framework import serializers
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', 'email')
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': False}
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Ride

class RideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ride
        fields = ('id', 'rider', 'driver', 'pickup_location', 'dropoff_location', 'status', 'created_at', 'updated_at', 'current_location')
        read_only_fields = ('id', 'status', 'created_at', 'updated_at')

    def validate_current_location(self, value):
        return value
    
    