# System
from django.db import IntegrityError
from rest_framework import viewsets, status

# Project
from core.auth import generate_access_token, generate_refresh_token
from core.constants import SYSTEM_CODE
from core.common import create_response
from core.exception import raise_exception
from app.users.models import User
from app.users.serializers.auth_serializers import RegisterSerializer, LoginSerializer


class AuthViewSet(viewsets.ViewSet):
    """
    인증 ViewSet
    """

    def post_register(self, request):
        """
        회원가입
        """
        serializer = RegisterSerializer(data=request.data)

        if not serializer.is_valid():
            raise_exception(code=SYSTEM_CODE.INVALID_FORMAT)

        try:
            user = User.objects.create_user(
                email=serializer.validated_data["email"],
                username=serializer.validated_data["username"],
                password=serializer.validated_data["password"],
            )
        except IntegrityError:
            raise_exception(code=SYSTEM_CODE.USER_ALREADY_EXIST)

        access_token = generate_access_token(user)
        refresh_token = generate_refresh_token(user)

        data = {
            "access_token": access_token,
            "refresh_token": refresh_token,
        }

        return create_response(data=data, status=status.HTTP_201_CREATED)

    def post_login(self, request):
        """
        로그인
        """
        serializer = LoginSerializer(data=request.data)

        if not serializer.is_valid():
            print(serializer.errors)
            raise_exception(code=SYSTEM_CODE.INVALID_FORMAT)

        user = User.objects.filter(email=serializer.validated_data["email"]).first()

        # 존재 하지 않는 유저
        if not user:
            raise_exception(code=SYSTEM_CODE.USER_NOT_FOUND)

        # 비밀번호 불일치
        if not user.check_password(serializer.validated_data["password"]):
            raise_exception(code=SYSTEM_CODE.USER_INVALID_PASSWORD)

        # 활성화 되지 않은 유저
        if not user.is_active:
            raise_exception(code=SYSTEM_CODE.USER_NOT_ACTIVE)

        access_token = generate_access_token(user)
        refresh_token = generate_refresh_token(user)

        data = {
            "access_token": access_token,
            "refresh_token": refresh_token,
        }

        return create_response(data=data, status=status.HTTP_200_OK)
