# System
from rest_framework import viewsets, status

# Project
from core.auth import auth_requred
from core.constants import SYSTEM_CODE
from core.common import create_response
from core.exception import raise_exception
from app.users.models import User


class UserViewSet(viewsets.ViewSet):
    """
    유저 ViewSet
    """

    @auth_requred
    def get_user(self, request):
        """
        유저 정보 조회
        """
        user = request.user

        data = {
            "email": user.email,
            "username": user.username,
        }

        return create_response(data=data, status=status.HTTP_200_OK)
