from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render


def home(request):
    return render(request, "lotto/home.html")


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)

        # 입력값이 올바르면 사용자를 생성하고 바로 로그인 처리
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("lotto:home")
    else:
        form = UserCreationForm()

    return render(request, "lotto/signup.html", {"form": form})