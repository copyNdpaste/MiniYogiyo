from django.db import models

from config.common_models import TimeStampedModel


class Category(TimeStampedModel):
    name = models.CharField(max_length=50, verbose_name="카테고리 이름")
    img = models.ImageField(blank=True, upload_to="category/", verbose_name="카테고리 이미지")

    def __str__(self):
        return self.name
