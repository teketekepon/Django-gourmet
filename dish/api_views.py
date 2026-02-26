"""料理系APIビュー。"""
from rest_framework import permissions, viewsets
from rest_framework.parsers import FormParser, MultiPartParser

from .api_serializers import CategorySerializer, DishCreateUpdateSerializer, DishSerializer
from .models import Category, Dish


class IsOwnerOrReadOnly(permissions.BasePermission):
    """所有者のみ更新・削除を許可する。"""

    def has_object_permission(self, request, view, obj) -> bool:
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """カテゴリ一覧・詳細API。"""

    queryset = Category.objects.order_by("id")
    serializer_class = CategorySerializer
    permission_classes = (permissions.AllowAny,)


class DishViewSet(viewsets.ModelViewSet):
    """料理一覧・詳細・作成・更新・削除API。"""

    queryset = Dish.objects.select_related("user", "category").order_by("-posted_at")
    permission_classes = (IsOwnerOrReadOnly,)
    parser_classes = (MultiPartParser, FormParser)

    def get_permissions(self):
        if self.action in ("list", "retrieve"):
            return [permissions.AllowAny()]
        if self.action == "create":
            return [permissions.IsAuthenticated()]
        return [permission() for permission in self.permission_classes]

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update"):
            return DishCreateUpdateSerializer
        return DishSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        category_id = self.request.query_params.get("category")
        user_id = self.request.query_params.get("user")
        mine = self.request.query_params.get("mine")

        if category_id:
            queryset = queryset.filter(category_id=category_id)
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        if mine == "true" and self.request.user.is_authenticated:
            queryset = queryset.filter(user=self.request.user)
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

