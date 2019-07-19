from django.urls import path
from . import views

urlpatterns = [
    path('logout/', views.LogoutApiView.as_view(), name='logout_api'),
    path('my_page/', views.MyPageApiView.as_view(), name='my_page_api'),
]
