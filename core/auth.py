# System
import functools
import jwt
from django.conf import settings
from datetime import datetime, timedelta, timezone
from rest_framework import status


# Project
from core.constants import SERVICE, SYSTEM_CODE
from app.users.models.users import User
from core.exception import raise_exception


def generate_access_token(user):
    """
    Generate Access Token
    """
    assert isinstance(user, User)

    payload = {
        "user_id": user.id,
        "email": user.email,
        "exp": datetime.now(tz=timezone.utc) + timedelta(minutes=SERVICE.ACCESS_TOKEN_EXP_MIN),
        "iat": datetime.now(tz=timezone.utc),
    }

    access_token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

    return access_token


def generate_refresh_token(user):
    """
    Generate Refresh Token
    """
    assert isinstance(user, User)

    payload = {
        "user_id": user.id,
        "email": user.email,
        "exp": datetime.now(tz=timezone.utc) + timedelta(days=SERVICE.REFRESH_TOKEN_EXP_DAY),
        "iat": datetime.now(tz=timezone.utc),
    }

    refresh_token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

    return refresh_token


def auth_requred(f):
    @functools.wraps(f)
    def wrap(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise_exception(code=SYSTEM_CODE.AUTH_REQUIRED, status=status.HTTP_403_FORBIDDEN)

        return f(self, request, *args, **kwargs)

    return wrap
