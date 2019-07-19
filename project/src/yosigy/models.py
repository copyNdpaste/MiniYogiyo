import enum

from django.db import models

from accounts.models import User
from config.common_models import TimeStampedModel
from menu.models import Menu
from restaurant.models import Restaurant


class YosigyTiketStatus(enum.IntEnum):
    NOT_PUBLISHED = 1
    PUBLISHED = 2
    USED = 3
    CANCEL = 4


STATUS_CHOICES = (
    (YosigyTiketStatus.NOT_PUBLISHED.value, '미발행'),
    (YosigyTiketStatus.PUBLISHED.value, '발행'),
    (YosigyTiketStatus.USED.value, '사용'),
    (YosigyTiketStatus.CANCEL.value, '취소')
)


class Yosigy(TimeStampedModel):
    restaurant = models.ForeignKey(
        Restaurant, on_delete=models.CASCADE, verbose_name="공구 제안한 레스토랑"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="사장님", related_name="owner"
    )
    deadline = models.DateField(verbose_name="마감기한")
    notice = models.TextField(blank=True, verbose_name="게시글")
    min_price = models.PositiveIntegerField(default=0, verbose_name="최소 주문 금액")

    def __str__(self):
        return "요식이 매장 : " + self.restaurant.name


class YosigyMenu(TimeStampedModel):
    discounted_price = models.PositiveIntegerField(
        default=0, verbose_name="할인된 메뉴 가격"
    )
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, verbose_name="메뉴")
    yosigy = models.ForeignKey(Yosigy, on_delete=models.CASCADE, verbose_name="요시기")

    def __str__(self):
        return str(self.yosigy.id) + " - " + self.menu.restaurant.title + self.menu.name + str(self.discounted_price)


class YosigyTicket(TimeStampedModel):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='식권 주인'
    )
    yosigy_menu = models.ForeignKey(
        YosigyMenu,
        on_delete=models.CASCADE,
        verbose_name='요시기 메뉴'
    )
    menu = models.ForeignKey(
        Menu,
        on_delete=models.CASCADE,
        verbose_name='요시기 메뉴에 해당하는 메뉴'
    )
    expire_time = models.DateTimeField()
    status = models.IntegerField(
        choices=STATUS_CHOICES,
        default=YosigyTiketStatus.NOT_PUBLISHED,
        verbose_name="상태"
    )

    def __str__(self):
        yosigy_enum = {1: '미발행',
                       2: '발행',
                       3: '사용됨',
                       4: '취소'}
        return (str(self.menu.id) + ' / ' +
                self.menu.name + ' / ' +
                str(yosigy_enum[self.status]) + ' / ' +
                self.user.username)


class TicketPayment(TimeStampedModel):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='티켓 구매자'
    )
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        verbose_name='구매한 레스토랑'
    )
    yosigy_ticket = models.ManyToManyField(
        YosigyTicket,
        verbose_name='사용할 요식이 티켓'
    )
    total_price = models.PositiveIntegerField(
        default=0,
        verbose_name='최종금액'
    )

    def __str__(self):
        return '-'.join([str(self.id), str(self.total_price) + '원'])
