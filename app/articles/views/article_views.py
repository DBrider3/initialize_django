# System
from django.db import IntegrityError
from rest_framework import status, viewsets


# Project
from core.constants import SYSTEM_CODE
from core.response import create_response
from core.exception import raise_exception
from core.auth import auth_requred
from core.pagination import CustomPagination
from app.articles.models import Article
from app.articles.serializers.article_serializers import (
    WriteArticleSerializer,
    ArticleSerializer,
)


class ArticleViewSet(viewsets.ViewSet):
    """
    게시판 ViewSet
    """

    def get_list_articles(self, request):
        """
        게시판 조회
        """

        pagination = CustomPagination()

        articles = Article.objects.all().order_by("-created_at")

        paginated_articles = pagination.paginate_queryset(articles, request)

        serializer = ArticleSerializer(paginated_articles, many=True)

        data = serializer.data

        response = pagination.get_paginated_response(data=data, status=status.HTTP_200_OK)

        return response

    def get_article(self, request, article_id):
        """
        게시글 조회
        """

        article = Article.objects.filter(id=article_id).first()

        if not article:
            raise_exception(code=SYSTEM_CODE.ARTICLE_NOT_FOUND)

        serializer = ArticleSerializer(article)

        data = serializer.data

        return create_response(data=data, status=status.HTTP_200_OK)

    @auth_requred
    def post_create_article(self, request):
        """
        게시글 생성
        """

        user = request.user

        serializer = WriteArticleSerializer(data=request.data)

        if not serializer.is_valid():
            raise_exception(code=SYSTEM_CODE.INVALID_FORMAT)

        title = serializer.validated_data.get("title")
        content = serializer.validated_data.get("content")

        try:
            Article.objects.create(title=title, content=content, author=user)
        except IntegrityError:
            raise_exception(status=SYSTEM_CODE.ARTICLE_CREATE_ERROR)

        return create_response(status=status.HTTP_201_CREATED)

    @auth_requred
    def patch_modify_article(self, request, article_id):
        """
        사용자의 게시글 수정
        """

        user = request.user

        article = Article.objects.filter(id=article_id, author=user).first()

        if not article:
            raise_exception(code=SYSTEM_CODE.ARTICLE_NOT_FOUND)

        serializer = WriteArticleSerializer(data=request.data)

        if not serializer.is_valid():
            raise_exception(code=SYSTEM_CODE.INVALID_FORMAT)

        title = serializer.validated_data.get("title")
        content = serializer.validated_data.get("content")

        article.title = title
        article.content = content
        article.save()

        return create_response(status=status.HTTP_200_OK)

    @auth_requred
    def get_user_article(self, request):
        """
        사용자의 게시글 조회
        """

        user = request.user

        articles = Article.objects.filter(author=user).order_by("-created_at")

        serializer = ArticleSerializer(articles, many=True)

        data = serializer.data

        return create_response(data=data, status=status.HTTP_200_OK)

    @auth_requred
    def delete_article(self, request, article_id):
        """
        게시글 삭제
        """

        user = request.user

        article = Article.objects.filter(id=article_id, author=user).first()

        if not article:
            raise_exception(code=SYSTEM_CODE.ARTICLE_NOT_FOUND)

        article.delete()

        return create_response(status=status.HTTP_200_OK)
