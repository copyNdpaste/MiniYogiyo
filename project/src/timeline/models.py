import enum
from django.db import models
from config.common_models import TimeStampedModel


class TimelineStatus(enum.IntEnum):
    CREATE = 1
    UPDATE = 2
    DELETE = 3


class TimelineType(enum.IntEnum):
    NOTICE = 1
    EVENT = 2
    OPERATION_HOUR = 3
    INFO = 4
    YOSIGY_EVENT = 5

    
STATUS_CHOICES = (
    (TimelineStatus.CREATE.value, '생성'),
    (TimelineStatus.UPDATE.value, '갱신'),
    (TimelineStatus.DELETE.value, '삭제')
)


TYPE_CHOICES = (
    (TimelineType.NOTICE.value, '사장님 알림'),
    (TimelineType.EVENT.value, '이벤트'),
    (TimelineType.OPERATION_HOUR.value, '운영시간'),
    (TimelineType.INFO.value, '기타 정보'),
    (TimelineType.YOSIGY_EVENT.value, '요식이 식권 이벤트')
)


class RestaurantTimelineComment(TimeStampedModel):
    restaurant_timeline = models.ForeignKey(
        'restaurant.restauranttimeline',
        on_delete=models.CASCADE,
        verbose_name='해당 타임라인'
    )
    writer = models.ForeignKey(
        'accounts.user',
        on_delete=models.CASCADE,
        verbose_name='댓글 작성자'
    )
    comment = models.TextField(
        verbose_name='댓글'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='댓글 활성화 여부'
    )

    def __str__(self):
        return '_'.join([str(self.id), str(self.writer), self.comment])


class MenuTimelineComment(TimeStampedModel):
    menu_timeline = models.ForeignKey(
        'menu.menutimeline',
        on_delete=models.CASCADE,
        verbose_name='해당 메뉴 타임라인'
    )
    writer = models.ForeignKey(
        'accounts.user',
        on_delete=models.CASCADE,
        verbose_name='댓글 작성자'
    )
    comment = models.TextField(
        verbose_name='댓글'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='댓글 활성화 여부'
    )

    def __str__(self):
        return '_'.join([str(self.id), str(self.writer), self.comment])
