from django.urls import path
from coupon import views

app_name = 'coupon'
urlpatterns = [
    path('gift_coupon/', views.gift_coupon, name='gift_coupon'),
    path('register_coupon/', views.register_coupon, name='register_gift_coupon'),
    path('register_coupon/<uuid:coupon_code>/', views.register_coupon_code, name='register_gift_coupon_code'),
    path('my_coupon/', views.my_coupon, name = 'my_coupon'),
    path('my_coupon/received_coupon/', views.received_coupon, name='received_coupon'),
    path('my_coupon/sent_coupon/', views.sent_coupon, name='sent_coupon'),
    path('my_coupon/available_coupon/', views.available_coupon, name='available_coupon')
]
