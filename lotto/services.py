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