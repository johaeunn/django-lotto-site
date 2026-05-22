from django.contrib import admin
from django.urls import path, include

from lotto import views as lotto_views

urlpatterns = [
    # 커스텀 관리자 페이지는 Django 기본 admin보다 먼저
    path("admin/dashboard/", lotto_views.admin_dashboard, name="admin_dashboard"),
    path("admin/draw/", lotto_views.admin_draw, name="admin_draw"),
    path("admin/results/", lotto_views.admin_results, name="admin_results"),

    path("admin/", admin.site.urls),

    # 기본 login 대신 커스텀 로그인 view를 사용
    path("login/", lotto_views.CustomLoginView.as_view(), name="login"),

    # Django 기본 로그인/로그아웃 URL
    path("", include("django.contrib.auth.urls")),

    # 로또 앱 URL
    path("", include("lotto.urls")),
]