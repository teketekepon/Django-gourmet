"""認証系APIビュー。"""
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import permissions, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken

from .api_serializers import SignUpSerializer, UserSerializer


User = get_user_model()


def _set_refresh_cookie(response: Response, refresh_token: str) -> None:
    cookie_settings = settings.JWT_AUTH
    response.set_cookie(
        key=cookie_settings["REFRESH_COOKIE_NAME"],
        value=refresh_token,
        httponly=True,
        secure=cookie_settings["REFRESH_COOKIE_SECURE"],
        samesite=cookie_settings["REFRESH_COOKIE_SAMESITE"],
        path=cookie_settings["REFRESH_COOKIE_PATH"],
    )


def _delete_refresh_cookie(response: Response) -> None:
    cookie_settings = settings.JWT_AUTH
    response.delete_cookie(
        key=cookie_settings["REFRESH_COOKIE_NAME"],
        path=cookie_settings["REFRESH_COOKIE_PATH"],
        samesite=cookie_settings["REFRESH_COOKIE_SAMESITE"],
    )


class SignUpApiView(APIView):
    """ユーザー登録API。"""

    permission_classes = (permissions.AllowAny,)

    def post(self, request: Request) -> Response:
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)


class LoginApiView(APIView):
    """ログインAPI。アクセストークンを返し、リフレッシュはCookieに保存する。"""

    permission_classes = (permissions.AllowAny,)

    def post(self, request: Request) -> Response:
        serializer = TokenObtainPairSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        access_token = serializer.validated_data["access"]
        refresh_token = serializer.validated_data["refresh"]

        response = Response({"access": access_token}, status=status.HTTP_200_OK)
        _set_refresh_cookie(response, refresh_token)
        return response


class RefreshApiView(APIView):
    """Cookie内リフレッシュトークンでアクセストークンを更新するAPI。"""

    permission_classes = (permissions.AllowAny,)

    def post(self, request: Request) -> Response:
        cookie_settings = settings.JWT_AUTH
        refresh_token = request.COOKIES.get(cookie_settings["REFRESH_COOKIE_NAME"])
        if not refresh_token:
            return Response({"detail": "refresh token not provided"}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)
            response = Response({"access": access_token}, status=status.HTTP_200_OK)

            if api_settings.ROTATE_REFRESH_TOKENS:
                if api_settings.BLACKLIST_AFTER_ROTATION:
                    try:
                        refresh.blacklist()
                    except AttributeError:
                        pass

                refresh.set_jti()
                refresh.set_exp(from_time=timezone.now())
                refresh.set_iat(at_time=timezone.now())
                _set_refresh_cookie(response, str(refresh))

            return response
        except TokenError:
            return Response({"detail": "invalid refresh token"}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutApiView(APIView):
    """ログアウトAPI。リフレッシュトークンを失効しCookieを削除する。"""

    permission_classes = (permissions.AllowAny,)

    def post(self, request: Request) -> Response:
        cookie_settings = settings.JWT_AUTH
        refresh_token = request.COOKIES.get(cookie_settings["REFRESH_COOKIE_NAME"])
        if refresh_token:
            try:
                RefreshToken(refresh_token).blacklist()
            except TokenError:
                pass

        response = Response(status=status.HTTP_204_NO_CONTENT)
        _delete_refresh_cookie(response)
        return response


class MeApiView(APIView):
    """ログインユーザー情報API。"""

    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request: Request) -> Response:
        return Response(UserSerializer(request.user).data, status=status.HTTP_200_OK)

