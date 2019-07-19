from datetime import datetime
from django import forms
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from coupon.models import GiftCoupon

INTERVAL_PRICE = 1000
MIN_PRICE = 5000
MAX_PRICE = 100000


class GiftCouponForm(forms.ModelForm):
    class Meta:
        model = GiftCoupon
        fields = (
            'receiver_name',
            'receiver_phone',
            'receiver_email',
            'sender_msg',
            'price')

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price < MIN_PRICE:
            raise forms.ValidationError('오천원 이상만 구매 가능합니다.')

        elif price >= MAX_PRICE:
            raise forms.ValidationError('십만원 이상만 구매 가능합니다.')

        elif not(price % INTERVAL_PRICE == 0):
            raise forms.ValidationError('천원단위로 금액을 선택해 주세요.')

        return price

    def clean_receiver_email(self):
        receiver_email = self.cleaned_data.get('receiver_email')
        try:
            validate_email(receiver_email)
        except ValidationError:
            raise forms.ValidationError('잘못된 이메일 입나다.')
        return receiver_email


class AvailableGiftCouponForm(forms.ModelForm):
    class Meta:
        model = GiftCoupon
        fields = (
            'is_used',
            'expire_date')

    def clean_is_used(self):
        is_used = self.cleaned_data.get('is_used')
        if is_used:
            raise forms.ValidationError('이미 사용된 쿠폰입니다.')
        return is_used

    def clean_expire_date(self):
        expire_date = self.cleaned_data.get('expire_date')
        if expire_date < datetime.now().date():
            raise forms.ValidationError('만료된 쿠폰입니다.')
        return expire_date
