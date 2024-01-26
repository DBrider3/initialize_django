# System
import jwt
from django.conf import settings
from rest_framework import viewsets, status

# Project
from core.auth import generate_access_token, generate_refresh_token
from core.constants import SYSTEM_CODE
from core.response import create_response
from core.exception import raise_exception
from core.times import get_now
from app.users.models.users import User
from app.users.serializers.auth_serializers import (
    RegisterSerializer,
    LoginSerializer,
    TokenRefreshSerializer,
)


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

        email = serializer.validated_data["email"]
        username = serializer.validated_data["username"]
        password = serializer.validated_data["password"]

        user = User.objects.create_user(email=email, username=username, password=password)

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

        # 로그인시 last_login 업데이트
        user.last_login = get_now()
        user.save()

        return create_response(data=data, status=status.HTTP_200_OK)

    def post_token_refresh(self, request):
        """
        refresh token으로 access token 재발급
        """

        serializer = TokenRefreshSerializer(data=request.data)

        if not serializer.is_valid():
            raise_exception(code=SYSTEM_CODE.INVALID_FORMAT)

        refresh_token = serializer.validated_data["refresh_token"]

        try:
            payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=["HS256"])

        # 토큰 만료
        except jwt.ExpiredSignatureError:
            raise_exception(code=SYSTEM_CODE.TOKEN_EXPIRED, status=status.HTTP_401_UNAUTHORIZED)

        # 토큰 부정확
        except jwt.DecodeError:
            raise_exception(code=SYSTEM_CODE.TOKEN_INVALID, status=status.HTTP_401_UNAUTHORIZED)

        user = User.objects.filter(id=payload["user_id"], email=payload["email"]).first()

        # 존재 하지 않는 유저
        if not user:
            raise_exception(code=SYSTEM_CODE.USER_NOT_FOUND, status=status.HTTP_401_UNAUTHORIZED)

        # 활성화 되지 않은 유저
        if not user.is_active:
            raise_exception(code=SYSTEM_CODE.USER_NOT_ACTIVE, status=status.HTTP_401_UNAUTHORIZED)

        access_token = generate_access_token(user)
        refresh_token = generate_refresh_token(user)

        data = {
            "access_token": access_token,
            "refresh_token": refresh_token,
        }

        return create_response(data=data, status=status.HTTP_200_OK)
