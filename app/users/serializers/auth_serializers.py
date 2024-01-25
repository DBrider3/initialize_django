# System
from rest_framework import serializers

# Project
from app.users.models.users import User


class RegisterSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255, required=True)
    username = serializers.CharField(max_length=255, required=True)
    password = serializers.CharField(max_length=128, required=True, write_only=True)


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255, required=True)
    password = serializers.CharField(max_length=128, required=True, write_only=True)


class TokenRefreshSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(max_length=1000, required=True)
