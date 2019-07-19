from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Post, Comment, Tag


# Register your models here.
# Blog.models.Post 모델에 대한 PostAdmin 커스텀
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # 보여줄 field
    list_display = ['id', 'title', 'content_size', 'status',
                    'create_date', 'update_date']
    actions = ['make_published', 'make_draft']

    def content_size(self, post):
        # mark_safe(): 태그 적용
        return mark_safe('<strong>{}글자</strong>'.format(len(post.content)))
    content_size.short_description = '글자수'  # 필드명 변경

    # action: 선택된 게시글의 status를 p(published)상태로 변경
    def make_published(self, request, queryset):
        update_count = queryset.update(status='p')  # QuerySet.update
        # django message framework 활용
        self.message_user(
            request, '{}건의 포스팅을 published 상태로 변경'.format(update_count))
    make_published.short_description = '지정 포스팅의 상태를 Published 상태로 변경'

    def make_draft(self, request, queryset):
        update_count = queryset.update(status='d')
        self.message_user(
            request, '{}건의 포스팅을 Draft 상태로 변경'.format(update_count))
    make_draft.short_description = '지정 포스팅의 상태를 Draft 상태로 변경'


# Blog.models.comment 모델에 대한  CommentAdmin 커스텀
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name']
    pass
