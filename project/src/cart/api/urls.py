from django.urls import path, reverse
from . import views

app_name = "cart_api"

urlpatterns = [
    path(
        '',
        views.CartListCreateAPIView.as_view(),
        name='cart_list_create_api'
    ),
    path(
        '<uuid:cart_id>/',
        views.CartItemCreateAPIView.as_view(),
        name='cart_item_create_api'
    ),
    path(
        '<uuid:cart_id>/menu/<int:menu_id>/',
        views.CartItemUpdateAPIView.as_view(),
        name='cart_item_update_delete_api'
    ),
    path(
        '<uuid:cart_id>/delete/',
        views.CartDeleteAPIView.as_view(),
        name='cart_delete_api'
    ),

    path(
        '<uuid:cart_id>/menu/<int:menu_id>/delete/',
        views.CartItemDeleteAPIView.as_view(),
        name='cart_item_delete_api'
    ),
    path(
        '<uuid:cart_id>/update/',
        views.CartItemUpdateAPIView.as_view(),
        name='cart_item_update_api'
    ),
    path(
        'quantity/',
        views.CartItemQuantityAPIView.as_view(),
        name='cart_item_quantity_api'
    ),

]
