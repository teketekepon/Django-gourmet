"""料理API用シリアライザ。"""
from rest_framework import serializers

from .models import Category, Dish


class CategorySerializer(serializers.ModelSerializer):
    """カテゴリ出力。"""

    class Meta:
        model = Category
        fields = ("id", "title")


class DishSerializer(serializers.ModelSerializer):
    """料理一覧・詳細出力。"""

    user_id = serializers.IntegerField(source="user.id", read_only=True)
    username = serializers.CharField(source="user.username", read_only=True)
    category_id = serializers.IntegerField(source="category.id", read_only=True)
    category_title = serializers.CharField(source="category.title", read_only=True)
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Dish
        fields = (
            "id",
            "user_id",
            "username",
            "category_id",
            "category_title",
            "title",
            "comment",
            "image_url",
            "posted_at",
        )

    def get_image_url(self, obj: Dish) -> str | None:
        if not obj.image:
            return None
        request = self.context.get("request")
        url = obj.image.url
        return request.build_absolute_uri(url) if request else url


class DishCreateUpdateSerializer(serializers.ModelSerializer):
    """料理作成・更新入力。"""

    class Meta:
        model = Dish
        fields = ("category", "title", "comment", "image")

