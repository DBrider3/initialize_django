# System
from django.urls import path, include

# Project
from app.users.views.auth_views import AuthViewSet
from app.users.views.user_views import UserViewSet

auth_urls = [
    path("register", AuthViewSet.as_view({"post": "post_register"})),
    path("login", AuthViewSet.as_view({"post": "post_login"})),
    path("refresh", AuthViewSet.as_view({"post": "post_token_refresh"})),
]

user_urls = [
    path("info", UserViewSet.as_view({"get": "get_user"})),
    path("password", UserViewSet.as_view({"patch": "patch_user_password"})),
]


urlpatterns = [
    path("auth/", include(auth_urls)),
    path("user/", include(user_urls)),
]
