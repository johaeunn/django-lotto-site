import random

from .models import LottoRound


def generate_lotto_numbers():
    """1~45 사이의 숫자 중 중복 없이 6개를 생성"""
    numbers = random.sample(range(1, 46), 6)
    numbers.sort()
    return numbers


def numbers_to_string(numbers):
    """숫자 리스트를 정렬한 뒤 DB 저장용 문자열로 변환"""
    sorted_numbers = sorted(numbers)
    return ",".join(map(str, sorted_numbers))


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