# System
from django.db import IntegrityError
from rest_framework import status, viewsets


# Project
from core.constants import SYSTEM_CODE
from core.response import create_response
from core.exception import raise_exception
from core.auth import auth_requred
from core.pagination import CustomPagination
from app.users.models import User
from app.articles.models import Article, Comment
from app.articles.serializers.comment_serializers import (
    WriteCommentSerializer,
    CommentSerializer,
)


class CommentViewSet(viewsets.ViewSet):
    """
    댓글 ViewSet
    """

    @auth_requred
    def post_create_comment(self, request, article_id):
        """
        댓글 생성
        """

        user = request.user

        article = Article.objects.filter(id=article_id).first()

        if not article:
            raise_exception(code=SYSTEM_CODE.ARTICLE_NOT_FOUND)

        serializer = WriteCommentSerializer(data=request.data)

        if not serializer.is_valid():
            raise_exception(code=SYSTEM_CODE.INVALID_FORMAT)

        validated_data = serializer.validated_data

        Comment.objects.create(**validated_data, article=article, author=user)

        return create_response(status=status.HTTP_201_CREATED)

    @auth_requred
    def get_list_comment(self, request, article_id):
        """
        댓글 리스트
        """

        pagination = CustomPagination()

        article = Article.objects.filter(id=article_id).first()

        if not article:
            raise_exception(code=SYSTEM_CODE.ARTICLE_NOT_FOUND)

        comments = Comment.objects.filter(article=article).order_by("-created_at")

        paginated_comments = pagination.paginate_queryset(comments, request)

        serializer = CommentSerializer(paginated_comments, many=True)

        data = serializer.data

        response = pagination.get_paginated_response(data=data, status=status.HTTP_200_OK)

        return response

    @auth_requred
    def patch_modify_comment(self, request, comment_id):
        """
        댓글 수정
        """

        user = request.user

        comment = Comment.objects.filter(id=comment_id, author=user).first()

        if not comment:
            raise_exception(code=SYSTEM_CODE.COMMENT_NOT_FOUND)

        serializer = WriteCommentSerializer(data=request.data)

        if not serializer.is_valid():
            raise_exception(code=SYSTEM_CODE.INVALID_FORMAT)

        content = serializer.validated_data["content"]

        comment.content = content
        comment.save()

        return create_response(status=status.HTTP_200_OK)

    @auth_requred
    def delete_comment(self, request, comment_id):
        """
        댓글 삭제
        """

        user = request.user

        comment = Comment.objects.filter(id=comment_id, author=user).first()
        if not comment:
            raise_exception(code=SYSTEM_CODE.COMMENT_NOT_FOUND)

        comment.delete()

        return create_response(status=status.HTTP_200_OK)
