from django.conf import settings
from django.db import models
from accounts.models import Taste
from config.common_models import TimeStampedModel
from restaurant.models import Restaurant
from timeline.models import STATUS_CHOICES

User = settings.AUTH_USER_MODEL


class Menu(TimeStampedModel):
    restaurant = models.ForeignKey(
        Restaurant, on_delete=True, verbose_name="연관되는 레스토랑")
    name = models.CharField(max_length=30, verbose_name="메뉴이름")
    img = models.ImageField(
        blank=True, upload_to="menu/%Y/%m/%d", verbose_name="메뉴이미지")
    detail = models.CharField(max_length=100, verbose_name="메뉴상세설명")
    price = models.IntegerField(default=0, verbose_name="메뉴가격")
    type = models.CharField(max_length=20, verbose_name="메뉴타입(인기메뉴,밥류...")
    tastes = models.ManyToManyField(
        Taste,
        blank=True,
        verbose_name='characteristics of menu'
    )
    hit = models.PositiveIntegerField("조회 수", default=0)
    like = models.ManyToManyField(
        User,
        blank=True,
        verbose_name='메뉴에 좋아요를 누른 사람'
    )
    score = models.FloatField('점수', default=0.0)
    is_recommended = models.BooleanField(
        '사장님 추천 메뉴인가?',
        default=False
    )
    is_yosigy = models.BooleanField(
        verbose_name='요식이 이벤트 여부',
        default=False,
    )
    is_set_menu = models.BooleanField(
        verbose_name='세트 메뉴 여부',
        default=False,
    )

    def __str__(self):
        return self.name


class MenuTimeLine(TimeStampedModel):
    menu = models.ForeignKey(Menu, verbose_name="모델 외래키", on_delete=models.CASCADE)
    status = models.IntegerField(choices=STATUS_CHOICES, verbose_name="생성1,갱신2,삭제3")
    prior_menu_img = models.ImageField(blank=True, upload_to="timeline/prior/menu/%Y/%m/%d", verbose_name="변경전 이미지")
    prior_menu_detail = models.CharField(blank=True, max_length=100, verbose_name="변경 전 메뉴상세설명")
    prior_menu_price = models.IntegerField(default=0, verbose_name="변경 전 메뉴가격")
    prior_menu_is_yosigy = models.BooleanField(blank=True, verbose_name="변경 전 요식이 메뉴 여부", default=False)
    prior_menu_is_set_menu = models.BooleanField(blank=True, verbose_name="변경 전 세트 메뉴 여부", default=False)
    post_menu_img = models.ImageField(blank=True, upload_to="timeline/post/menu/%Y/%m/%d", verbose_name="변경된 이미지")
    post_menu_detail = models.CharField(blank=True, max_length=100, verbose_name="변경 후 메뉴상세설명")
    post_menu_price = models.IntegerField(default=0, verbose_name="변경 후 메뉴가격")
    post_menu_is_yosigy = models.BooleanField(blank=True, verbose_name="변경 후 요식이 메뉴 여부", default=False)
    post_menu_is_set_menu = models.BooleanField(blank=True, verbose_name="변경 후 세트 메뉴 여부", default=False)
    is_recommended = models.BooleanField(blank=True, verbose_name='사장님 추천 메뉴인가?', default=False)
    like = models.ManyToManyField(
        User,
        blank=True,
        verbose_name='메뉴에 좋아요를 누른 사람'
    )
