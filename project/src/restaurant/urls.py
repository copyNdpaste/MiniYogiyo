from django.urls import path
from . import views

app_name = 'restaurant'

urlpatterns = [
    path(
        'category/<int:category_id>/restaurant/',
        views.restaurant_list,
        name='restaurant_list'
    ),
    path(
        'category/<int:category_id>/restaurant/<int:restaurant_id>/',
        views.restaurant_detail,
        name='restaurant_detail'
    )
]
