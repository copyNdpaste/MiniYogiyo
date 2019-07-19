from django.db import models

from config.common_models import TimeStampedModel


class Grid(TimeStampedModel):
    name = models.CharField(max_length=20, verbose_name='행정동 이름 ex 서초2동')
    x = models.PositiveSmallIntegerField(verbose_name='x 좌표')
    y = models.PositiveSmallIntegerField(verbose_name='y 좌표')

    def __str__(self):
        return self.name
