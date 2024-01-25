# System
import traceback
from rest_framework.exceptions import APIException
from rest_framework import status


# Project
from core.constants import SYSTEM_CODE, SERVICE
from core.common import create_response


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
