# System
from rest_framework import serializers


# Project
from app.users.models.users import User


class UpdateUserPasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=128, required=True)
    new_password = serializers.CharField(max_length=128, required=True)
