# System
import traceback
import jwt
from django.conf import settings
from datetime import datetime, timedelta
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import APIException
from rest_framework import status


# Project
from core.constants import SYSTEM_CODE, SERVICE
from core.common import create_response
from core.exception import raise_exception
from app.users.models.users import User


class CustomJWTAuthentication(BaseAuthentication):
    """
    Custom JWT Authentication
    """

    def authenticate(self, request):
        # Extract the JWT from the Authorization header
        authorization_header = request.headers.get("Authorization", None)
        if authorization_header is None:
            return None

        access_token = authorization_header.split(" ")[1]

        # Decode the JWT and verify its signature
        try:
            payload = jwt.decode(access_token, settings.SECRET_KEY, algorithms=["HS256"])

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

        return user, None


def custom_api_exception_handler(exc, context):
    """
    Custom Api Exception Handler
    """

    if isinstance(exc, APIException):
        payload = {
            "data": getattr(exc, "data", None),
            "code": getattr(exc, "code", SYSTEM_CODE.UNKNOWN_SERVER_ERROR),
            "status": getattr(exc, "status_code"),
            "extra": getattr(exc, "extra", None),
        }
        return create_response(**payload)

    if exc.__class__.__name__ == "DoesNotExist":
        return create_response(code=SYSTEM_CODE.OBJECT_DOES_NOT_EXIST, status=status.HTTP_404_NOT_FOUND)

    if SERVICE.DEBUG:
        # Print Unexpected Error Message to Console in Debug
        print(traceback.format_exc())

    return create_response(
        code=SYSTEM_CODE.UNKNOWN_SERVER_ERROR,
        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )
