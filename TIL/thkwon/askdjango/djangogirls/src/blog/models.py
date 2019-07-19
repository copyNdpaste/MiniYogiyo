
from django.db import models
from django.utils import timezone
from django.shortcuts import reverse


class Post(models.Model):
    author = models.ForeignKey(
        "auth.User",
        related_name="post_authors",
        on_delete=models.CASCADE
    )
    title = models.CharField(
        verbose_name="제목",
        max_length=200
    )
    text = models.TextField(
        verbose_name="내용",
    )
    created_date = models.DateTimeField(
        verbose_name="생성시간",
        default=timezone.now
    )
    published_date = models.DateTimeField(
        verbose_name="발행시간",
        blank=True,
        null=True
    )

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog:post_detail", kwargs={"post_id": self.pk})

    def approved_comments(self):
        return self.comments.filter(approved_comment=True)


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        related_name='comments',
        on_delete=True
    )
    author = models.ForeignKey(
        "auth.User",
        related_name="comment_authors",
        on_delete=models.CASCADE
    )
    text = models.TextField(
        verbose_name="내용",
    )
    created_date = models.DateTimeField(
        verbose_name="생성시간",
        default=timezone.now
    )
    approved_comment = models.BooleanField(
        verbose_name="승인여부",
        default=False
    )

    class Meta:
        ordering = ['-id']

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text
