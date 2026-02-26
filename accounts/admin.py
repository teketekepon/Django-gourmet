"""admin モジュール。"""
from django.contrib import admin
from .models import CustomUser

class CustomUserAdmin(admin.ModelAdmin):
    """CustomUserAdmin の責務を表すクラス。"""
    # idとusernameを表示する
    list_display: tuple[str, str] = ('id', 'username')
    # リンクを設定する
    list_display_links: tuple[str, str] = ('id', 'username')


admin.site.register(CustomUser, CustomUserAdmin)
