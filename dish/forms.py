"""forms モジュール。"""
from django.forms import ModelForm
from .models import Dish

class DishForm(ModelForm):
    """DishForm の責務を表すクラス。"""
    class Meta:
        """Meta の責務を表すクラス。"""
        model = Dish
        fields: list[str] = ['category', 'title', 'comment', 'image']
