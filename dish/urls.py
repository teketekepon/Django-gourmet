"""urls モジュール。"""
from django.urls import path
from django.urls.resolvers import URLPattern, URLResolver
from . import views

# URLパターンを逆引きできるように名前を付ける
app_name: str = 'dish'

# URLパターンを登録する変数
urlpatterns: list[URLPattern | URLResolver] = [
    path('', views.IndexView.as_view(), name='index'),
    path('post/', views.CreateDishView.as_view(), name='post'),
    path('post_done/', views.PostSuccessView.as_view(), name='post_done'),
    
    # カテゴリ一覧ページ
    path('dishs/<int:category>', views.CategoryView.as_view(), name = 'dishs_cat'),

    # ユーザーリスト覧ページ
    path('user-list/<int:user>', views.UserView.as_view(), name = 'user_list'),
    
    # 詳細ページ
    path('dish-detail/<int:pk>', views.DetailView.as_view(), name = 'dish_detail'),
    
    # マイページ
    # mypage/へのアクセスはMypageViewを実行
    path('mypage/', views.MypageView.as_view(), name = 'mypage'),

    # 投稿写真の削除
    path('dish/<int:pk>/delete/',
         views.DishDeleteView.as_view(),
         name = 'dish_delete'
         ),
]
