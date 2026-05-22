from django.conf import settings
from django.db import models


class LottoRound(models.Model):
    round_number = models.PositiveIntegerField(
        unique=True,
        verbose_name="회차 번호",
    )
    winning_numbers = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="당첨 번호",
    )
    bonus_number = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="보너스 번호",
    )
    is_drawn = models.BooleanField(
        default=False,
        verbose_name="추첨 완료 여부",
    )
    drawn_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="추첨 일시",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="생성 일시",
    )

    class Meta:
        ordering = ["-round_number"]
        verbose_name = "로또 회차"
        verbose_name_plural = "로또 회차 목록"

    def __str__(self):
        return f"{self.round_number}회차"


class Ticket(models.Model):
    PURCHASE_TYPE_MANUAL = "manual"
    PURCHASE_TYPE_AUTO = "auto"

    PURCHASE_TYPE_CHOICES = [
        (PURCHASE_TYPE_MANUAL, "수동"),
        (PURCHASE_TYPE_AUTO, "자동"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="tickets",
        verbose_name="구매자",
    )
    lotto_round = models.ForeignKey(
        LottoRound,
        on_delete=models.CASCADE,
        related_name="tickets",
        verbose_name="로또 회차",
    )
    numbers = models.CharField(
        max_length=100,
        verbose_name="구매 번호",
    )
    purchase_type = models.CharField(
        max_length=10,
        choices=PURCHASE_TYPE_CHOICES,
        verbose_name="구매 방식",
    )
    purchased_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="구매 일시",
    )

    class Meta:
        ordering = ["-purchased_at"]
        verbose_name = "구매 복권"
        verbose_name_plural = "구매 복권 목록"

    def __str__(self):
        return f"{self.user.username} - {self.lotto_round.round_number}회차 - {self.numbers}"