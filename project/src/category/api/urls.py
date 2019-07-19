from django.urls import path
from . import views


app_name="category_api"

urlpatterns = [
    path(
        '',
        views.CategoryListAPIView.as_view(),
        name='category_list_api'
    ),
]
