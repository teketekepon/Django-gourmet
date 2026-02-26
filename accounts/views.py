"""views モジュール。"""
from django.forms import BaseModelForm
from django.http import HttpResponse
from django.views.generic import CreateView, TemplateView
from .forms import CustomUserCreationForm
from django.urls import reverse_lazy

class SignUpView(CreateView):
    """SignUpView の責務を表すクラス。"""
    form_class = CustomUserCreationForm
    template_name = "signup.html"
    success_url = reverse_lazy('accounts:signup_success')

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        """form_valid を実行する。"""
        user = form.save()
        self.object = user
        return super().form_valid(form)

class SignUpSuccessView(TemplateView):
    """SignUpSuccessView の責務を表すクラス。"""
    template_name = "signup_success.html"
