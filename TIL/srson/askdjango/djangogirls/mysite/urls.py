"""mysite URL Configuration
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
]
