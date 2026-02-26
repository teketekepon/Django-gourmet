"""views モジュール。"""
from django.db.models import QuerySet
from django.forms import BaseModelForm
from django.http import HttpRequest, HttpResponse, HttpResponseBase
from django.views.generic import TemplateView, ListView
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import DetailView
from django.views.generic import DeleteView
from .models import Dish
from .forms import DishForm

class IndexView(ListView):
    """IndexView の責務を表すクラス。"""
    template_name = 'index.html'
    queryset: QuerySet[Dish] = Dish.objects.order_by('-posted_at')

@method_decorator(login_required, name='dispatch')
class CreateDishView(CreateView):
    """CreateDishView の責務を表すクラス。"""
    form_class = DishForm
    template_name = "post_dish.html"
    success_url = reverse_lazy('dish:post_done')

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        """form_valid を実行する。"""
        postdata = form.save(commit=False)
        postdata.user = self.request.user
        postdata.save()
        return super().form_valid(form)

class PostSuccessView(TemplateView):
    """PostSuccessView の責務を表すクラス。"""
    template_name ='post_success.html'

class CategoryView(ListView):
    """CategoryView の責務を表すクラス。"""
    template_name ='index.html'

    def get_queryset(self) -> QuerySet[Dish]:
      """get_queryset を実行する。"""
      category_id = self.kwargs['category']
      categories = Dish.objects.filter(category=category_id).order_by('-posted_at')
      return categories

class UserView(ListView):
    """UserView の責務を表すクラス。"""
    template_name ='index.html'

    def get_queryset(self) -> QuerySet[Dish]:
      """get_queryset を実行する。"""
      user_id = self.kwargs['user']
      user_list = Dish.objects.filter(
        user=user_id).order_by('-posted_at')
      return user_list

class DetailView(DetailView):
    """DetailView の責務を表すクラス。"""
    template_name ='detail.html'
    model = Dish

class MypageView(LoginRequiredMixin, ListView):
    """MypageView の責務を表すクラス。"""
    template_name ='mypage.html'
    login_url = reverse_lazy('accounts:login')

    def get_queryset(self) -> QuerySet[Dish]:
      """get_queryset を実行する。"""
      queryset = Dish.objects.filter(
        user=self.request.user).order_by('-posted_at')
      return queryset
  
class DishDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """DishDeleteView の責務を表すクラス。"""
    model = Dish
    template_name ='dish_delete.html'
    success_url = reverse_lazy('dish:mypage')
    login_url = reverse_lazy('accounts:login')

    def test_func(self) -> bool:
      """test_func を実行する。"""
      dish = self.get_object()
      return dish.user == self.request.user

    def handle_no_permission(self) -> HttpResponseBase:
      """handle_no_permission を実行する。"""
      if self.request.user.is_authenticated:
        return HttpResponse(status=403)
      return super().handle_no_permission()

    def delete(self, request: HttpRequest, *args: object, **kwargs: object) -> HttpResponse:
      """delete を実行する。"""
      return super().delete(request, *args, **kwargs)
