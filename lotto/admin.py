from django.contrib import admin

from .models import LottoRound, Ticket


@admin.register(LottoRound)
class LottoRoundAdmin(admin.ModelAdmin):
    list_display = (
        "round_number",
        "winning_numbers",
        "bonus_number",
        "is_drawn",
        "drawn_at",
        "created_at",
    )
    list_filter = (
        "is_drawn",
        "created_at",
        "drawn_at",
    )
    search_fields = (
        "round_number",
    )
    ordering = (
        "-round_number",
    )
    readonly_fields = (
        "created_at",
    )


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "lotto_round",
        "numbers",
        "purchase_type",
        "purchased_at",
    )
    list_filter = (
        "purchase_type",
        "lotto_round",
        "purchased_at",
    )
    search_fields = (
        "user__username",
        "numbers",
    )
    ordering = (
        "-purchased_at",
    )
    readonly_fields = (
        "purchased_at",
    )