from django.urls import path
from . import views

app_name = 'menu'

urlpatterns = [
    path(
        'category/<int:category_id>/menu/',
        views.menu_list,
        name='menu_list',
    ),
    path(
        'category/<int:category_id>/restaurant/<int:restaurant_id>/menu/<int:menu_id>/',
        views.menu_detail,
        name='menu_detail',
    ),
    path(
        'random_menu_pick/',
        views.random_menu_pick_list,
        name='random_menu_pick_list',
    ),
]
