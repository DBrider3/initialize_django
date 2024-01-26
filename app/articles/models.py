# System
from django.db import models
from django.conf import settings

# Project
from core.models import BaseModel
from app.users.models import User


class Article(BaseModel):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        related_name="articles",
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.title


class Comment(BaseModel):
    content = models.TextField()
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name="comments",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        related_name="comments",
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.content
