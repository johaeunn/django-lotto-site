from django.urls import path
from . import views

app_name = "lotto"

urlpatterns = [
    path("", views.home, name="home"),
    path("signup/", views.signup, name="signup"),
    path("buy/auto/", views.buy_auto, name="buy_auto"),
]