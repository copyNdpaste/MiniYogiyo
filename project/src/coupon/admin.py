from django.contrib import admin
from coupon.models import GiftCoupon, UserGiftCoupon


@admin.register(GiftCoupon)
class GiftCouponAdmin(admin.ModelAdmin):
    fields = ('sender', 'receiver_name', 'receiver_phone', 'receiver_email', 'price', 'expire_date')
    list_display = ('id', 'coupon_code', 'expire_date', 'sender', 'receiver_name',)


@admin.register(UserGiftCoupon)
class UserGiftCouponAdmin(admin.ModelAdmin):
    fields = ('gift_coupon', 'user', 'prior_user', 'is_owner', 'is_registrant')
    list_display = ('id', 'gift_coupon', 'user', 'is_owner', 'is_registrant',)
