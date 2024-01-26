# System

from rest_framework import pagination
from rest_framework.response import Response

# Project
from core.constants import SYSTEM_CODE


class CustomPagination(pagination.PageNumberPagination):
    page_size = 2

    def get_paginated_response(self, **kwargs):
        status = kwargs.get("status", 200)
        headers = kwargs.get("headers", None)

        data = kwargs.get("data", None)

        code = kwargs.get("code", SYSTEM_CODE.SUCCESS)

        msg = kwargs.get("msg", code[1])

        extra = kwargs.get("extra", None)

        payload = {
            "links": {
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
            },
            "count": self.page.paginator.count,
            "data": data,
            "msg": msg,
            "code": code[0],
            "extra": extra,
        }

        return Response(payload, status=status, headers=headers)
