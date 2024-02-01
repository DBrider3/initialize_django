# System
from django.db import models
from django.conf import settings

# Project
from core.models import BaseModel


class Article(BaseModel):
    title = models.CharField(max_length=255)
    content = models.TextField(null=True, blank=True)
    thumbnail = models.ImageField(blank=True)

    author = models.ForeignKey(
        "users.User",
        on_delete=models.DO_NOTHING,
        related_name="article_user",
        blank=True,
        null=True,
    )

    class Meta:
        app_label = "articles"
        db_table = "article"

    def __str__(self):
        return self.title


class Comment(BaseModel):
    content = models.TextField()
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name="comment_article",
    )
    author = models.ForeignKey(
        "users.User",
        on_delete=models.DO_NOTHING,
        related_name="comment_user",
        blank=True,
        null=True,
    )

    class Meta:
        app_label = "articles"
        db_table = "comment"

    def __str__(self):
        return self.content
