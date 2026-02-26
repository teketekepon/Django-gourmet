"""models モジュール。"""
from django.db import models
from accounts.models import CustomUser

# 料理のカテゴリー
class Category(models.Model):
    """Category の責務を表すクラス。"""
    title = models.CharField( verbose_name='カテゴリ', max_length=20)

    def __str__(self) -> str:
        """__str__ を実行する。"""
        return self.title

class Dish(models.Model):
    """Dish の責務を表すクラス。"""
    user = models.ForeignKey(
        CustomUser, verbose_name='ユーザー', on_delete=models.CASCADE
    )

    category = models.ForeignKey(
        Category, verbose_name='カテゴリ', on_delete=models.PROTECT
    )

    title = models.CharField(
        verbose_name='タイトル', max_length=200
    )

    comment = models.TextField(
        verbose_name='コメント', default='コメントはありません'
    )

    image = models.ImageField(
        verbose_name='イメージ', upload_to='dishs', blank=True
    )

    posted_at = models.DateTimeField(
        verbose_name='投稿日時', auto_now_add=True
    )

    def __str__(self) -> str:
        """__str__ を実行する。"""
        return self.title
