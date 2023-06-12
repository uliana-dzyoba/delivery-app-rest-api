from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model

from authentication.models import CustomUserManager


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

    def validate_password(self, password):
        validate_password(password)
        return password

    def validate_email(self, email):
        norm_email = CustomUserManager.normalize_email(email)
        if get_user_model().objects.filter(email=norm_email).exists():
            raise serializers.ValidationError("Not unique email")
        return norm_email

    def create(self, validated_data):
        user = get_user_model()(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
