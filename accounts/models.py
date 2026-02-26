"""models モジュール。"""
from django.db import models
from django.contrib.auth.models import AbstractUser

# Userモデルを継承したカスタムユーザーモデル
class CustomUser(AbstractUser):
    """CustomUser の責務を表すクラス。"""
    pass
