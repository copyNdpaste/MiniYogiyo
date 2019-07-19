from django.urls import path

from . import views

app_name = "grouppurchase"

urlpatterns = [
    path(
        '',
        views.grouppurchase_list,
        name='list',
    ),
    path(
        '<int:grouppurchase_id>/',
        views.grouppurchase_detail,
        name='detail',
    ),
    path(
        'create/',
        views.grouppurchase_create,
        name='create',
    ),
]
