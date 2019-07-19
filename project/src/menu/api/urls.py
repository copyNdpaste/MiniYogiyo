from django.urls import path
from . import views

app_name = 'menu_api'

urlpatterns = [
    path(
        'api/category/<int:category_id>/restaurant/<int:restaurant_id>/menu/',
        views.MenuListAPIView.as_view(),
        name='menu_list_api'
    ),
    path(
        'api/category/<int:category_id>/restaurant/<int:restaurant_id>/menu/<int:menu_id>/',
        views.MenuDetailAPIView.as_view(),
        name='menu_detail_api'
    ),
    path(
        'api/category/<int:category_id>/menu/',
        views.MenuListAPIView.as_view(),
        name='menu_list_api'
    ),
    path(
        'api/random_menu_pick/',
        views.RandomMenuListAPIView.as_view(),
        name='random_menu_list_api',
    ),
    path(
        'api/random_menu_pick/already_eaten/',
        views.AlreadyEatenMenuRandomListAPIView.as_view(),
        name='already_eaten_random_menu_list_api',
    ),
]
