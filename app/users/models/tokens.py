# System
from django.conf import settings
from django.db import models

# Project
from core.models import BaseModel


class Token(BaseModel):
    """
    Token Model
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="users_token",
    )
    refresh_token = models.CharField(max_length=1000, null=True)

    class Meta:
        db_table = "users_tokens"
        app_label = "users"

    def __str__(self):
        return self.token
