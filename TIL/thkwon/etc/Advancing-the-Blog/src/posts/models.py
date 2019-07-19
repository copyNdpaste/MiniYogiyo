from django.db import models
from django.shortcuts import reverse


class Post(models.Model):
    title = models.CharField(
        "제목",
        max_length=120
    )
    content = models.TextField(
        "내용"
    )
    updated = models.DateTimeField(
        "업데이트 시간",
        auto_now=True
    )
    timestamp = models.DateTimeField(
        "생성 시간",
        auto_now_add=True
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("posts:post_detail", kwargs={"id": self.id})
