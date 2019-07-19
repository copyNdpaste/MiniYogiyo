from django.urls import path
from . import views

app_name = 'restaurant_api'

urlpatterns = [
    path(
        'api/category/<int:category_id>/restaurant/',
        views.RestaurantListAPIView.as_view(),
        name='restaurant_list_api'
    ),
    path(
        'api/category/<int:category_id>/restaurant/<int:restaurant_id>/',
        views.RestaurantDetailAPIView.as_view(),
        name='restaurant_detail_api'
    ),
    path(
        'api/subscribe/restaurant/<int:restaurant_id>/',
        views.RestaurantSubscribeCreateAPIView.as_view(),
        name='restaurant_subscribe_api'
    ),

    path(
        'api/subscribed_restaurants/',
         views.SubscribedRestaurantsAPIView.as_view(),
         name='subscribed_restaurant_api'
     ),
]
