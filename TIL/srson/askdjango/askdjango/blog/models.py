import re
from django.conf import settings
from django.forms import ValidationError
from django.db import models


def lnglat_validator(value):
    if not re.match(r'^([+-]?\d+\.?\d*),([+-]?\d+\.?\d*)$', value):
        # 조건에 맞지 않으면 예외 발생
        raise ValidationError('Invalid LngLat Type')


# Create your models here.
class Post(models.Model):
    STATUS_CHOICES = {
        ('d', 'Draft'),
        ('p', 'Published'),
        ('w', 'Withdrawn'),
    }

    username = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT,
        related_name='blog_post_set')
    title = models.CharField(max_length=100, verbose_name='제목')
    content = models.TextField(verbose_name='내용')
    tags = models.CharField(max_length=100, blank=True)
    lnglat = models.CharField(
        max_length=50, blank=True,
        validators=[lnglat_validator],  # 함수 자체를 넘겨서 유효성 검사시 이 함수 호출하여 사용
        help_text='경도/위도 포맷으로 입력')
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    tag_set = models.ManyToManyField('Tag', blank=True)
    create_date = models.DateField(auto_now_add=True)  # auto_now_add 최초 일시 저장
    update_date = models.DateTimeField(auto_now=True)  # auto_now 갱신마다 일시 저장

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    comments = models.TextField()
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=False)

    def __str__(self):
        return self.comments


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
