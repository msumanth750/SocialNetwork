from .models import UserProfile
from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password','username']


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','email', 'first_name','last_name','username']


class UserProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name' , read_only=True)
    last_name = serializers.CharField(
        source='user.last_name', read_only=True)

    class Meta:
        model = UserProfile
        fields = '__all__'
