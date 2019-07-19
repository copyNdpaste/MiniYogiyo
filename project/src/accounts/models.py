from django.contrib.auth.models import AbstractUser
from django.db import models
from config.common_models import TimeStampedModel
from restaurant.models import Restaurant


class Taste(TimeStampedModel):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name


class User(AbstractUser):
    phone = models.CharField(max_length=15, blank=True)
    address = models.CharField(max_length=50, blank=True)
    address_detail = models.CharField(max_length=50, blank=True)
    user_type = models.IntegerField(
        default=1,
        blank=True,
        null=True,
        help_text='1: user, 2: restaurant_owner')
    deactivate_date = models.DateField(blank=True, null=True)
    tastes = models.ManyToManyField(
        Taste,
        blank=True,
        verbose_name='user\'s tastes',
    )
    subscribed_restaurants = models.ManyToManyField(
        Restaurant,
        blank=True,
        verbose_name='구독 레스토랑',
        related_name='subscribers',
    )
