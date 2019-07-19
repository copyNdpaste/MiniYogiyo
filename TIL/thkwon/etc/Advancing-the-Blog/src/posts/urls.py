from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path(
        '',
        views.post_list,
        name='post_list'
    ),
    path(
        'create/',
        views.post_create,
        name='post_create'
    ),

    path(
        '<int:id>/',
        views.post_detail,
        name='post_detail'
    ),
    path(
        '<int:id>/update/',
        views.post_update,
        name='post_update'
    ),
    path(
        '<int:id>/delete/',
        views.post_delete,
        name='post_delete'
    ),


]
