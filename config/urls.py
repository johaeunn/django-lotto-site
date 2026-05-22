from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # 나중에 커스텀 관리자 URL은 admin.site.urls보다 위에 둔다.
    path("admin/", admin.site.urls),

    # Django 기본 로그인/로그아웃 URL
    path("", include("django.contrib.auth.urls")),

    # 로또 앱 URL
    path("", include("lotto.urls")),
]