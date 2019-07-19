from django.urls import path

from yosigy import views

app_name = "yosigy"

urlpatterns = [
    path(
        '',
        views.yosigy_list,
        name='list',
    ),
    path(
        '<int:yosigy_id>/',
        views.yosigy_detail,
        name='detail',
    ),
    path(
        'create/',
        views.yosigy_create,
        name='create',
    ),
    path(
        'order/list/',
        views.yosigy_order_list,
        name='order_list',
    ),
]
