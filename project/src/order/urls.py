from django.urls import path
from . import views

app_name = 'order'

urlpatterns = [

    path(
        '',
        views.OrderView.as_view(),
        name='order_list'
    ),
    path(
        'history/',
        views.OrderHistoryListView.as_view(),
        name='order_history'
    )

]
