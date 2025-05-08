from django.contrib import admin
from django.urls import path
from attendance import views
from django.views.generic import RedirectView

urlpatterns = [
    # 初期アクセスで登録用パスワードページへ
    path('', RedirectView.as_view(url='/signup/password/', permanent=False)),

    # 登録用パスワード認証
    path('signup/password/', views.signup_password, name='signup_password'),
    # 出欠登録フォーム
    path('signup/', views.signup, name='signup'),

    # 一覧閲覧用パスワード認証
    path('records/password/', views.admin_password, name='admin_password'),
    # 参加者一覧
    path('records/', views.admin_list, name='admin_list'),

    # Django 管理サイト
    path('admin/', admin.site.urls),
]