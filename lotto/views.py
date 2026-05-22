from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render
from django.contrib.admin.views.decorators import staff_member_required

from .forms import ManualLottoPurchaseForm
from .models import Ticket
from .models import LottoRound, Ticket
from .services import (
    attach_results_to_tickets,
    draw_lotto_round,
    generate_lotto_numbers,
    get_all_round_statistics,
    get_current_lotto_round,
    numbers_to_string,
    string_to_numbers,
)


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


@login_required
def buy_manual(request):
    """사용자가 직접 선택한 번호로 로또를 구매한다."""
    lotto_numbers = range(1, 46)

    if request.method == "POST":
        form = ManualLottoPurchaseForm(request.POST)

        if form.is_valid():
            lotto_round = get_current_lotto_round()
            numbers = form.cleaned_data["numbers"]
            numbers_text = numbers_to_string(numbers)

            ticket = Ticket.objects.create(
                user=request.user,
                lotto_round=lotto_round,
                numbers=numbers_text,
                purchase_type=Ticket.PURCHASE_TYPE_MANUAL,
            )

            return render(request, "lotto/purchase_done.html", {"ticket": ticket})
    else:
        form = ManualLottoPurchaseForm()

    return render(
        request,
        "lotto/buy_manual.html",
        {
            "form": form,
            "numbers": lotto_numbers,
        },
    )


@login_required
def my_tickets(request):
    """로그인한 사용자의 구매 내역과 당첨 결과를 조회"""
    tickets = (
        Ticket.objects
        .filter(user=request.user)
        .select_related("lotto_round")
        .order_by("-purchased_at")
    )

    tickets = attach_results_to_tickets(tickets)

    return render(request, "lotto/my_tickets.html", {"tickets": tickets})


@login_required
def results(request):
    """추첨 완료된 복권의 당첨 결과를 따로 조회"""
    tickets = (
        Ticket.objects
        .filter(user=request.user, lotto_round__is_drawn=True)
        .select_related("lotto_round")
        .order_by("-lotto_round__round_number", "-purchased_at")
    )

    tickets = attach_results_to_tickets(tickets)

    return render(request, "lotto/results.html", {"tickets": tickets})


@staff_member_required
def admin_draw(request):
    """관리자가 현재 판매 중인 회차의 추첨을 실행"""
    current_round = (
        LottoRound.objects
        .filter(is_drawn=False)
        .order_by("-round_number")
        .first()
    )

    drawn_round = None
    winning_numbers = []

    if request.method == "POST":
        # 판매 중인 회차가 없다면 새 회차를 생성한 뒤 추첨
        if current_round is None:
            current_round = get_current_lotto_round()

        drawn_round = draw_lotto_round(current_round)
        winning_numbers = string_to_numbers(drawn_round.winning_numbers)

        # 추첨 완료 후 다음 구매를 위한 새 회차를 미리 생성
        get_current_lotto_round()

    return render(
        request,
        "lotto/admin_draw.html",
        {
            "current_round": current_round,
            "drawn_round": drawn_round,
            "winning_numbers": winning_numbers,
        },
    )


@staff_member_required
def admin_dashboard(request):
    """관리자용 전체 현황 대시보드를 표시"""
    total_ticket_count = Ticket.objects.count()
    total_round_count = LottoRound.objects.count()
    drawn_round_count = LottoRound.objects.filter(is_drawn=True).count()

    current_round = (
        LottoRound.objects
        .filter(is_drawn=False)
        .order_by("-round_number")
        .first()
    )

    recent_tickets = (
        Ticket.objects
        .select_related("user", "lotto_round")
        .order_by("-purchased_at")[:10]
    )

    context = {
        "total_ticket_count": total_ticket_count,
        "total_round_count": total_round_count,
        "drawn_round_count": drawn_round_count,
        "current_round": current_round,
        "recent_tickets": recent_tickets,
    }

    return render(request, "lotto/admin_dashboard.html", context)


@staff_member_required
def admin_results(request):
    """관리자용 판매/당첨 통계 페이지를 표시"""
    round_statistics = get_all_round_statistics()

    total_ticket_count = Ticket.objects.count()
    total_drawn_round_count = LottoRound.objects.filter(is_drawn=True).count()

    context = {
        "round_statistics": round_statistics,
        "total_ticket_count": total_ticket_count,
        "total_drawn_round_count": total_drawn_round_count,
    }

    return render(request, "lotto/admin_results.html", context)
