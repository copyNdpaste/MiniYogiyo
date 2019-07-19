import enum
import uuid

from django.conf import settings
from django.db import models

from config.common_models import TimeStampedModel
from cart.models import Cart
from coupon.models import GiftCoupon
from restaurant.models import Restaurant
from yosigy.models import YosigyTicket

User = settings.AUTH_USER_MODEL


class DeliveryStatus(enum.IntEnum):
    WATING = 0
    DELIVERING = 1
    COMPLETE = 2


class PaymentWay(enum.IntEnum):
    ON_SITE_CASH = 0
    ON_SITE_CREDIT = 1


class PaymentStatus(enum.IntEnum):
    IN_PROGRESS = 0
    ACCEPT = 1
    CANCEL = 2


STATUS_CHOICES = (
    (PaymentStatus.IN_PROGRESS.value, '결제 진행 중'),
    (PaymentStatus.ACCEPT.value, '결제 승인'),
    (PaymentStatus.CANCEL.value, '결제 취소')
)

PAYMENT_CHOICES = (
    (PaymentWay.ON_SITE_CASH.value, '현장결제 - 현금'),
    (PaymentWay.ON_SITE_CREDIT.value, '현장결제 - 카드')
)

DELIVERY_CHOICES = (
    (DeliveryStatus.WATING.value, '대기 중'),
    (DeliveryStatus.DELIVERING.value, '배달 중'),
    (DeliveryStatus.COMPLETE.value, '배달 완료')
)


class OrderQuerySet(models.QuerySet):
    def history_list(self, logged_in_user):
        return (self
                .select_related(
                    'user',
                    'cart',
                    'restaurant',
                    'gift_coupon'
                )
                .filter(
                    user=logged_in_user
                )
                .values(
                    'id',
                    'restaurant__img',
                    'restaurant__title',
                    'created_time',
                    'delivery_status',
                    'status',
                    'total_price',
                    'user__id',
                    'address',
                    'address_detail',
                    'phone_num',
                    'payment_status',
                    'restaurant__min_order_price',
                    'restaurant__delivery_charge',
                    'cart_id',
                    'yosigy_ticket',
                    'yosigy_ticket__menu__name',
                    'yosigy_ticket__menu__img',
                    'yosigy_ticket__menu__detail',
                    'gift_coupon',
                    'gift_coupon__price',
                    'gift_coupon__coupon_code'
                )
                .order_by('-created_time')
                )


class OrderManager(models.Manager):
    def get_queryset(self):
        return OrderQuerySet(self.model, using=self._db)

    def history_list(self, logged_in_user):
        return self.get_queryset().history_list(logged_in_user)


class Order(TimeStampedModel, OrderManager):
    id = models.UUIDField(
        '주문 식별번호',
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    user = models.ForeignKey(
        User,
        verbose_name='주문자',
        on_delete=models.CASCADE
    )
    cart = models.ForeignKey(
        Cart,
        verbose_name='주문표',
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )
    restaurant = models.ForeignKey(
        Restaurant,
        verbose_name='해당 주문관련 레스토랑',
        on_delete=models.CASCADE
    )
    total_price = models.IntegerField(
        '주문 총 가격',
        default=0
    )
    address = models.CharField(
        '주문자 주소',
        max_length=200
    )
    address_detail = models.CharField(
        '주문자 상세 주소',
        max_length=200
    )
    status = models.IntegerField(
        '주문 상태 정보',
        choices=STATUS_CHOICES,
        default=PaymentStatus.IN_PROGRESS
    )
    delivery_status = models.IntegerField(
        '배달 상태 정보',
        choices=DELIVERY_CHOICES,
        default=DeliveryStatus.WATING
    )
    weather = models.PositiveSmallIntegerField(
        '주문 당시 날씨 정보',
        default=0
    )
    phone_num = models.CharField(
        '전화번호',
        max_length=13
    )
    payment_status = models.IntegerField(
        '주문 결제 상태 정보',
        choices=PAYMENT_CHOICES,
        default=PaymentWay.ON_SITE_CASH
    )
    gift_coupon = models.OneToOneField(
        GiftCoupon,
        verbose_name='주문시 사용 쿠폰',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    yosigy_ticket = models.ManyToManyField(
        YosigyTicket,
        blank=True,
        verbose_name='사용한 요시기 식권'
    )
    objects = OrderManager()

    def __str__(self):
        return self.user.username + " - " + self.restaurant.name + " - weather : " + str(self.weather)
