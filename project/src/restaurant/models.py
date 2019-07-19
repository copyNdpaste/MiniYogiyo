from django.db import models
from django.conf import settings
from category.models import Category
from config.common_models import TimeStampedModel
from timeline import models as timeline

User = settings.AUTH_USER_MODEL


class Restaurant(TimeStampedModel):
    category = models.ManyToManyField(Category, verbose_name="레스토랑에 관련된 카테고리")
    name = models.CharField(max_length=50, verbose_name="업체명")
    owner = models.CharField(max_length=20, verbose_name="사장님 이름")
    store_owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='store_owner', verbose_name="사장님 계정")
    title = models.CharField(max_length=50, verbose_name="업체명+기타문구(x치킨-서초점)")
    img = models.ImageField(blank=True, upload_to="restaurant/%Y/%m/%d", verbose_name="레스토랑 이미지")
    tel = models.CharField(max_length=13, verbose_name="전화번호")
    min_order_price = models.IntegerField(verbose_name="최소주문금액", default=0)
    order_way = models.CharField(max_length=15, verbose_name="주문방식")
    origin = models.TextField(verbose_name="원산지")
    delivery_charge = models.IntegerField(verbose_name="배달요금", default=0)
    info = models.TextField(verbose_name="사장님 알림말")
    event = models.TextField(verbose_name='이벤트', blank=True)
    event_img = models.ImageField(blank=True, upload_to='restaurant/event/%Y/%m/%d', verbose_name='event image')
    type = models.CharField(max_length=50, verbose_name="레스토랑타입(요기요등록음식점)")
    estimated_delivery_time = models.TimeField(verbose_name="배달예상시간")
    operation_start_hour = models.TimeField(verbose_name="영업시작시간")
    operation_end_hour = models.TimeField(verbose_name="영업종료시간")
    like = models.ManyToManyField(
        User,
        blank=True,
        verbose_name='레스토랑에 좋아요를 누른 사람'
    )
    is_yosigy = models.BooleanField(
        verbose_name='요식이 이벤트 진행 여부',
        default=False
    )

    def __str__(self):
        return self.name


class RestaurantTimeline(TimeStampedModel):
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        verbose_name='restaurant')
    status = models.IntegerField(
        verbose_name='상태',
        choices=timeline.STATUS_CHOICES,
        default=timeline.TimelineStatus.UPDATE
    )
    changed_data = models.TextField(
        verbose_name='변경 사항 내용',
        blank=True
    )
    changed_img = models.ImageField(
        verbose_name='변경 사진',
        upload_to='timeline/%Y/%m/%d',
        blank=True
    )
    prior_info = models.CharField(
        verbose_name='변경 전 정보',
        max_length=50,
        blank=True
    )
    post_info = models.CharField(
        verbose_name='변경 후 정보',
        max_length=50,
        blank=True
    )
    timeline_type = models.IntegerField(
        verbose_name='변경 사항',
        choices=timeline.TYPE_CHOICES,
        default=timeline.TimelineType.NOTICE
    )
    like = models.ManyToManyField(
        User,
        blank=True,
        verbose_name='좋아요를 누른 사람'
    )
    changed_field = models.CharField(
        verbose_name='변경된 field',
        max_length=50
    )
    yosigy = models.ForeignKey(
        'yosigy.yosigy',
        on_delete=models.CASCADE,
        null=True,
        verbose_name='요식이 이벤트'
    )

    def __str__(self):
        return ' '.join([self.get_timeline_type_display(), self.get_status_display()])
