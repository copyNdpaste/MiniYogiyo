from django.urls import path

from yosigy.api import yosigy_ticket_list_views
from . import yosigy_list_views, yosigy_detail_views, yosigy_create_views,\
    yosigy_order_list_views, yosigy_order_views, yosigy_ticket_payment_views


app_name = 'yosigy_api'

urlpatterns = [
    path(
        'list/<int:category_id>/page/<int:page>/',
        yosigy_list_views.YosigyListAPIView.as_view(),
        name='yosigy_list_api'
    ),
    path(
        'detail/<int:yosigy_id>/',
        yosigy_detail_views.YosigyDetailAPIView.as_view(),
        name='yosigy_detail_api'
    ),
    path(
        'create/',
        yosigy_create_views.YosigyCreateAPIView.as_view(),
        name='yosigy_create_api'
    ),
    path(
        'create/<int:restaurant_id>/',
        yosigy_create_views.YosigyMenuListAPIView.as_view(),
        name='yosigy_create_menu_api'
    ),
    path(
       'payment/list/',
        yosigy_ticket_payment_views.YosigyTicketPaymentListAPIView.as_view(),
        name='yosigy_payment_list_api'
    ),
    path(
       'payment/list/<int:ticket_payment_id>/',
        yosigy_ticket_payment_views.YosigyTicketPaymentDetailAPIView.as_view(),
        name='yosigy_payment_detail_api'
    ),
    path(
        'ticket/list/',
        yosigy_ticket_list_views.YosigyTicketListAPIView.as_view(),
        name='yosigy_ticket_list_api'
    ),
    path(
        'order/list/',
        yosigy_order_list_views.YosigyOrderListAPIView.as_view(),
        name='yosigy_order_list_api'
    ),
    path(
        'order/',
        yosigy_order_views.YosigyOrderAPIView.as_view(),
        name='yosigy_order_api'
    ),
    path(
        'ticket/<int:restaurant_id>/',
        yosigy_detail_views.YosigyTicketCreateAPIView.as_view(),
        name='yosigy_create_ticket_api'
    )
]
