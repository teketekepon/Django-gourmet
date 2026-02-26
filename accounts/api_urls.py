"""認証APIのURL定義。"""
from django.urls import path

from .api_views import LoginApiView, LogoutApiView, MeApiView, RefreshApiView, SignUpApiView


urlpatterns = [
    path("signup/", SignUpApiView.as_view(), name="api_signup"),
    path("login/", LoginApiView.as_view(), name="api_login"),
    path("refresh/", RefreshApiView.as_view(), name="api_refresh"),
    path("logout/", LogoutApiView.as_view(), name="api_logout"),
    path("me/", MeApiView.as_view(), name="api_me"),
]

