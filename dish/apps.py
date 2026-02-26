"""apps モジュール。"""
from django.apps import AppConfig


class DishConfig(AppConfig):
    """DishConfig の責務を表すクラス。"""
    default_auto_field: str = 'django.db.models.BigAutoField'
    name: str = 'dish'
