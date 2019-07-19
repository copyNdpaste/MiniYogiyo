from django.urls import path

from . import views

app_name = "order_api"

urlpatterns = [
    path(
        '',
        views.OrderCreateDetailAPIView.as_view(),
        name='order_create_detail'
    ),
    path(
        'history/',
        views.OrderHistoryListAPIView.as_view(),
        name='order_history_list'
    ),
    path(
        'reorder/<uuid:order_id>/',
        views.ReOrderCreateAPIView.as_view(),
        name='reorder'
    ),
]
