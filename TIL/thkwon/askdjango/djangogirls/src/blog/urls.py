from django.urls import path
from . import views

app_name = "blog"

urlpatterns = [
    path(
        '',
        views.post_list,
        name='post_list'
    ),
    path(
        '<int:post_id>/',
        views.post_detail,
        name='post_detail'
    ),
    path(
        'new/',
        views.post_new,
        name='post_new'
    ),
    path(
        '<int:post_id>/edit/',
        views.post_edit,
        name='post_edit'
    ),
    path(
        'drafts/',
        views.post_draft_list,
        name='post_draft_list'
    ),
    path(
        '<int:post_id>/publish/',
        views.post_publish,
        name='post_publish'
    ),
    path(
        '<int:post_id>/remove/',
        views.post_remove,
        name='post_remove'
    ),
    path(
        '<int:post_id>/comment/',
        views.comment_new,
        name='comment_new'
    ),
    path(
        '<int:comment_id>/comment_remove/',
        views.comment_remove,
        name='comment_remove'
    ),
    path(
        '<int:comment_id>/comment_approve/',
        views.comment_approve,
        name='comment_approve'
    ),
]
