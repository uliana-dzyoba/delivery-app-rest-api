from rest_framework import serializers
# from .models import User
from django.contrib.auth import get_user_model


class UserPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'email']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = '__all__'


class UserSignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'phone_number', 'address', 'password']

    def create(self, validated_data):
        user = get_user_model()(**validated_data)

        user.set_password(validated_data['password'])
        user.save()

        return user


