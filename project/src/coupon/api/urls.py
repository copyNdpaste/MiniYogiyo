from django.urls import path
from coupon.api import views

urlpatterns = [
    path('create_gift_coupon/', views.GiftCouponApiCreate.as_view(), name='create_gift_coupon_api'),
    path('register_gift_coupon/', views.GiftCouponRegisterApi.as_view(), name='register_gift_coupon_api'),
    path('received_coupon_list/', views.ReceivedCouponListApi.as_view(), name='received_coupon_list_api'),
    path('sent_coupon_list/', views.SentCouponListApi.as_view(), name='sent_coupon_list_api'),
    path('available_coupon_list/', views.AvailableCouponListApi.as_view(), name='available_coupon_list_api'),
    path('use_coupon/<int:registered_coupon_id>/', views.CouponUseApi.as_view(), name='coupon_use_api'),
    path('unchecked_coupon_list/', views.UncheckedHandoverCouponListApi.as_view(), name='unchecked_coupon_list'),
]
