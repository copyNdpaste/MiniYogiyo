import uuid
from django.db import models
from config.common_models import TimeStampedModel
from accounts.models import User


class GiftCoupon(TimeStampedModel):
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE,
        verbose_name='보낸 사람')
    sender_msg = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='메세지 입력')
    receiver_name = models.CharField(
        max_length=15,
        verbose_name='받는 사람')
    receiver_phone = models.CharField(
        max_length=15,
        blank=True,
        verbose_name='받는 사람 연락처')
    receiver_email = models.CharField(
        max_length=50,
        verbose_name='받는 사람 이메일')
    expire_date = models.DateField(
        verbose_name='쿠폰 만료일')
    coupon_code = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        verbose_name='쿠폰번호')
    price = models.PositiveIntegerField(
        verbose_name='금액')
    is_used = models.BooleanField(
        default=False,
        verbose_name='사용함')
    used_date = models.DateField(
        null=True,
        verbose_name='사용한 날짜')

    def __str__(self):
        return str(self.coupon_code)


class UserGiftCoupon(TimeStampedModel):
    gift_coupon = models.ForeignKey(
        GiftCoupon,
        on_delete=models.CASCADE,
        verbose_name='gift coupon')
    user = models.ForeignKey(
        User,
        related_name='user',
        on_delete=models.CASCADE,
        verbose_name='쿠폰 사용자')
    prior_user = models.ForeignKey(
        User,
        related_name='prior_user',
        null=True,
        on_delete=models.CASCADE,
        verbose_name='양도 해준 사람')
    is_owner = models.BooleanField(
        default=True,
        verbose_name='쿠폰 사용가능자')
    is_registrant = models.BooleanField(
        default=True,
        verbose_name='쿠폰 등록자')
    is_checked = models.BooleanField(
        default=False,
        verbose_name='받은 쿠폰 확인'
    )

    def __str__(self):
        return str(self.gift_coupon)
