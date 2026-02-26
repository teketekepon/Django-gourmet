"""forms モジュール。"""
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    """CustomUserCreationForm の責務を表すクラス。"""
    class Meta:
        """Meta の責務を表すクラス。"""
        model = CustomUser
        fields: tuple[str, str, str, str] = ('username', 'email', 'password1', 'password2')
