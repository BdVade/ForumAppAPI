from rest_framework import serializers
from .models import User


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number', 'display_picture', 'date_joined']

class ProfileEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['phone_number', 'display_picture', ]

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']
        read_only_fields = ['username']