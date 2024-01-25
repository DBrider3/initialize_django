# System
from rest_framework import serializers

# Project
from app.users.models import User


class RegisterSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255, required=True)
    username = serializers.CharField(max_length=255, required=True)
    password = serializers.CharField(max_length=128, required=True, write_only=True)


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255, required=True)
    password = serializers.CharField(max_length=128, required=True, write_only=True)
