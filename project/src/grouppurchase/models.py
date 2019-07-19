import enum

from django.conf import settings
from django.db import models

from config.common_models import TimeStampedModel
from menu.models import Menu
from restaurant.models import Restaurant
from grouppurchase import helper

User = settings.AUTH_USER_MODEL


class GrouppurchaseStatus(enum.IntEnum):
    BEFORE = 1,
    INPROGRESS = 2,
    COMPLETE = 3,


STATUS_CHOICES = (
    (GrouppurchaseStatus.BEFORE.value, "진행 전"),
    (GrouppurchaseStatus.INPROGRESS.value, "진행 중"),
    (GrouppurchaseStatus.COMPLETE.value, "완료"),
)


class GroupPurchase(TimeStampedModel):
    restaurant = models.ForeignKey(
        Restaurant, on_delete=models.CASCADE, verbose_name="공구 제안한 레스토랑"
    )
    menu = models.ForeignKey(
        Menu, on_delete=models.CASCADE, verbose_name="공구할 메뉴"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="공구 글 작성자", related_name="writer"
    )
    deadline = models.DateField(verbose_name="마감기한")
    target_number = models.PositiveIntegerField(default=0, verbose_name="목표 인원")
    status = models.IntegerField(choices=STATUS_CHOICES, verbose_name="공구 상태")
    participant = models.ManyToManyField(User, blank=True, verbose_name="현재 참여자")
    notice = models.TextField(blank=True, verbose_name="게시글")


class Message(TimeStampedModel):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='받는 사람'
    )
    contents = models.TextField(
        verbose_name='내용')
    is_checked = models.BooleanField(
        verbose_name='확인 여부',
        default=False)
