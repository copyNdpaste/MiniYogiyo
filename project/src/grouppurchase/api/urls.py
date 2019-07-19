from django.urls import path
from . import board_views

app_name = 'grouppurchase_api'

urlpatterns = [
    path(
        'api/grouppurchase/board/',
        board_views.BoardAPIView.as_view(),
        name='board_api'
    ),
]
