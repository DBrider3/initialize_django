# System
from rest_framework import serializers

# Project
from core.constants import SYSTEM_CODE
from core.exception import raise_exception
from app.users.models.users import User


class RegisterSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255, required=True)
    username = serializers.CharField(max_length=255, required=True)
    password = serializers.CharField(max_length=128, required=True, write_only=True)

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise_exception(code=SYSTEM_CODE.USER_ALREADY_EXIST)
        return value


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255, required=True)
    password = serializers.CharField(max_length=128, required=True, write_only=True)


class TokenRefreshSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(max_length=1000, required=True)
