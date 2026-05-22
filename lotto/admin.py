from django.contrib import admin

from .models import LottoRound, Ticket


@admin.register(LottoRound)
class LottoRoundAdmin(admin.ModelAdmin):
    # Admin 목록 화면에 표시할 필드
    list_display = (
        "round_number",
        "winning_numbers",
        "bonus_number",
        "is_drawn",
        "drawn_at",
        "created_at",
    )

    # 오른쪽 필터 영역에 표시할 항목
    list_filter = (
        "is_drawn",
        "created_at",
        "drawn_at",
    )

    # 검색 가능한 필드
    search_fields = (
        "round_number",
    )

    # 기본 정렬: 최신 회차가 위로 오도록 설정
    ordering = (
        "-round_number",
    )

    # Admin 상세 화면에서 읽기 전용으로 표시할 필드
    readonly_fields = (
        "created_at",
    )


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    # Admin 목록 화면에 표시할 필드
    list_display = (
        "id",
        "user",
        "lotto_round",
        "numbers",
        "purchase_type",
        "purchased_at",
    )

    # 구매 방식과 회차 기준으로 필터링 가능
    list_filter = (
        "purchase_type",
        "lotto_round",
        "purchased_at",
    )

    # 사용자명과 구매 번호로 검색 가능
    search_fields = (
        "user__username",
        "numbers",
    )

    # 최신 구매 내역이 위로 오도록 설정
    ordering = (
        "-purchased_at",
    )

    # 구매 시간은 자동 생성되므로 수정하지 않도록 설정
    readonly_fields = (
        "purchased_at",
    )