from django.urls import path

from .views import (
            UpdateModelDetailAPIView,
            UpdateModelListAPIView
)


urlpatterns = [
    path(
        '<int:id>/',
        UpdateModelDetailAPIView.as_view()
    ),
    path(
        '',
        UpdateModelListAPIView.as_view(),
    ),
]