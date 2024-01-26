# System
from rest_framework import viewsets, status

# Project
from core.auth import auth_requred
from core.constants import SYSTEM_CODE
from core.common import create_response
from core.exception import raise_exception
from app.users.models.users import User
from app.users.serializers.user_serializers import UpdateUserPasswordSerializer


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

    @auth_requred
    def patch_user_password(self, request):
        """
        비밀번호 변경
        """
        user = request.user

        serializer = UpdateUserPasswordSerializer(data=request.data)

        if not serializer.is_valid():
            raise_exception(code=SYSTEM_CODE.INVALID_FORMAT)

        if not user.check_password(serializer.validated_data["old_password"]):
            raise_exception(code=SYSTEM_CODE.USER_INVALID_PASSWORD)

        user.set_password(serializer.validated_data["new_password"])
        user.save()

        return create_response(status=status.HTTP_200_OK)
