import random

from django.utils import timezone

from .models import LottoRound


def generate_lotto_numbers():
    """1~45 사이의 숫자 중 중복 없이 6개를 생성"""
    numbers = random.sample(range(1, 46), 6)
    numbers.sort()
    return numbers


def generate_bonus_number(winning_numbers):
    """당첨 번호와 겹치지 않는 보너스 번호를 생성"""
    candidates = [
        number
        for number in range(1, 46)
        if number not in winning_numbers
    ]
    return random.choice(candidates)


def numbers_to_string(numbers):
    """숫자 리스트를 정렬한 뒤 DB 저장용 문자열로 변환"""
    sorted_numbers = sorted(numbers)
    return ",".join(map(str, sorted_numbers))


def string_to_numbers(numbers_text):
    """DB에 저장된 번호 문자열을 숫자 리스트로 변환"""
    if not numbers_text:
        return []

    return [
        int(number)
        for number in numbers_text.split(",")
        if number
    ]


def get_current_lotto_round():
    """
    현재 판매할 로또 회차를 가져오기
    추첨되지 않은 회차가 없으면 다음 회차를 새로 생성
    """
    current_round = (
        LottoRound.objects
        .filter(is_drawn=False)
        .order_by("-round_number")
        .first()
    )

    if current_round:
        return current_round

    last_round = LottoRound.objects.order_by("-round_number").first()

    if last_round:
        next_round_number = last_round.round_number + 1
    else:
        next_round_number = 1

    return LottoRound.objects.create(round_number=next_round_number)

def draw_lotto_round(lotto_round):
    """전달받은 회차에 대해 당첨 번호와 보너스 번호를 저장"""
    winning_numbers = generate_lotto_numbers()
    bonus_number = generate_bonus_number(winning_numbers)

    lotto_round.winning_numbers = numbers_to_string(winning_numbers)
    lotto_round.bonus_number = bonus_number
    lotto_round.is_drawn = True
    lotto_round.drawn_at = timezone.now()
    lotto_round.save()

    return lotto_round


def calculate_rank(ticket_numbers, winning_numbers, bonus_number):
    """구매 번호와 당첨 번호를 비교해 등수를 계산"""
    ticket_set = set(ticket_numbers)
    winning_set = set(winning_numbers)

    matched_count = len(ticket_set & winning_set)
    matched_bonus = bonus_number in ticket_set if bonus_number else False

    if matched_count == 6:
        rank = 1
    elif matched_count == 5 and matched_bonus:
        rank = 2
    elif matched_count == 5:
        rank = 3
    elif matched_count == 4:
        rank = 4
    elif matched_count == 3:
        rank = 5
    else:
        rank = 0

    return {
        "rank": rank,
        "matched_count": matched_count,
        "matched_bonus": matched_bonus,
    }


def get_rank_display(rank):
    """등수 숫자를 화면 표시용 문자열로 변환"""
    if rank == 0:
        return "낙첨"

    return f"{rank}등"


def get_ticket_result(ticket):
    """
    복권 한 장의 당첨 결과를 계산
    추첨 전 회차라면 결과 대신 '추첨 전' 상태를 반환
    """
    lotto_round = ticket.lotto_round

    if not lotto_round.is_drawn:
        return {
            "status": "pending",
            "display": "추첨 전",
            "rank": None,
            "matched_count": None,
            "matched_bonus": None,
            "winning_numbers": [],
            "bonus_number": None,
        }

    ticket_numbers = string_to_numbers(ticket.numbers)
    winning_numbers = string_to_numbers(lotto_round.winning_numbers)

    result = calculate_rank(
        ticket_numbers=ticket_numbers,
        winning_numbers=winning_numbers,
        bonus_number=lotto_round.bonus_number,
    )

    return {
        "status": "drawn",
        "display": get_rank_display(result["rank"]),
        "rank": result["rank"],
        "matched_count": result["matched_count"],
        "matched_bonus": result["matched_bonus"],
        "winning_numbers": winning_numbers,
        "bonus_number": lotto_round.bonus_number,
    }


def attach_results_to_tickets(tickets):
    """템플릿에서 사용하기 쉽도록 각 Ticket 객체에 result 속성 추가"""
    for ticket in tickets:
        ticket.result = get_ticket_result(ticket)

    return tickets

def get_round_statistics(lotto_round):
    """특정 회차의 판매 수와 등수별 당첨 통계를 계산."""
    tickets = (
        lotto_round.tickets
        .select_related("user", "lotto_round")
        .order_by("-purchased_at")
    )

    rank_counts = {
        1: 0,
        2: 0,
        3: 0,
        4: 0,
        5: 0,
        0: 0,
    }

    for ticket in tickets:
        result = get_ticket_result(ticket)

        # 추첨 전 회차는 등수 계산 대상에서 제외
        if result["status"] != "drawn":
            continue

        rank_counts[result["rank"]] += 1

    return {
        "round": lotto_round,
        "ticket_count": tickets.count(),
        "rank_1_count": rank_counts[1],
        "rank_2_count": rank_counts[2],
        "rank_3_count": rank_counts[3],
        "rank_4_count": rank_counts[4],
        "rank_5_count": rank_counts[5],
        "losing_count": rank_counts[0],
    }


def get_all_round_statistics():
    """전체 회차의 판매/당첨 통계를 최신 회차 순으로 계산"""
    lotto_rounds = (
        LottoRound.objects
        .prefetch_related("tickets")
        .order_by("-round_number")
    )

    return [
        get_round_statistics(lotto_round)
        for lotto_round in lotto_rounds
    ]