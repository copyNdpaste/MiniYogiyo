from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
  path('top_view/', views.top_view, name='top_view'),
  path('my_page/', views.my_page, name='my_page'),
]
