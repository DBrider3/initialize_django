# System
from django.urls import path, include

# Project
from app.articles.views.article_views import ArticleViewSet
from app.articles.views.comment_views import CommentViewSet

article_urls = [
    path("", ArticleViewSet.as_view({"get": "get_list_articles"})),
    path("create", ArticleViewSet.as_view({"post": "post_create_article"})),
    path("<int:article_id>", ArticleViewSet.as_view({"get": "get_article"})),
    path(
        "modify/<int:article_id>",
        ArticleViewSet.as_view({"patch": "patch_modify_article"}),
    ),
    path("user", ArticleViewSet.as_view({"get": "get_user_article"})),
    path("delete/<int:article_id>", ArticleViewSet.as_view({"delete": "delete_article"})),
]

comment_urls = [
    path("<int:article_id>", CommentViewSet.as_view({"get": "get_list_comment"})),
    path(
        "<int:article_id>/create",
        CommentViewSet.as_view({"post": "post_create_comment"}),
    ),
    path(
        "<int:comment_id>/modify",
        CommentViewSet.as_view({"patch": "patch_modify_comment"}),
    ),
    path(
        "<int:comment_id>/delete",
        CommentViewSet.as_view({"delete": "delete_comment"}),
    ),
]

urlpatterns = [
    path("article/", include(article_urls)),
    path("comment/", include(comment_urls)),
]
