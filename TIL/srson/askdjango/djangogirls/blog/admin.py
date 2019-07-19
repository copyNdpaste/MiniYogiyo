from django.contrib import admin
from .models import Comment, Post


# Register your models here.
admin.site.register(Post)  # admin에 등록


admin.site.register(Comment)  # admin에 comment 모델 등록
