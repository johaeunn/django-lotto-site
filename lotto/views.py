from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render

from .models import Ticket
from .services import generate_lotto_numbers, get_current_lotto_round, numbers_to_string


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

@login_required
def buy_auto(request):
    """
    로그인한 사용자가 자동 번호로 로또를 구매
    GET 요청으로 직접 구매되는 것을 막기 위해 POST 요청만 처리
    """
    if request.method != "POST":
        return redirect("lotto:home")

    lotto_round = get_current_lotto_round()
    numbers = generate_lotto_numbers()
    numbers_text = numbers_to_string(numbers)

    ticket = Ticket.objects.create(
        user=request.user,
        lotto_round=lotto_round,
        numbers=numbers_text,
        purchase_type=Ticket.PURCHASE_TYPE_AUTO,
    )

    return render(request, "lotto/purchase_done.html", {"ticket": ticket})