from datetime import datetime
from django import forms

from coupon.models import GiftCoupon
from order.models import Order


class OrderModelForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = (
            'user',
            'cart',
            'restaurant',
            'total_price',
            'address',
            'address_detail',
            'phone_num',
            'payment_status',
            'gift_coupon',
            'weather',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.gift_coupon_obj = False

    def clean_phone_num(self):
        phone_num = self.cleaned_data.get('phone_num')
        phone_num_list = phone_num.split("-")
        if not(len(phone_num_list) == 3 and phone_num_list[0] == '010'):
            raise forms.ValidationError('올바르지 않은 폰 번호 입니다.')
        return phone_num

    def clean_gift_coupon(self):
        gift_coupon = self.cleaned_data.get('gift_coupon')

        if gift_coupon and gift_coupon is not None:
            gift_coupon_qs = (
                GiftCoupon.objects.filter(
                    pk=gift_coupon.id,
                    usergiftcoupon__is_owner=True,
                    usergiftcoupon__user=self.cleaned_data.get('user').id
                ))

            try:
                gift_coupon_obj = gift_coupon_qs[0]
                self.gift_coupon_obj = gift_coupon_obj
            except IndexError:
                raise forms.ValidationError('사용할 수 없는 쿠폰 입니다.')

            total_price = self.cleaned_data.get('total_price')
            if gift_coupon_obj.price > total_price:
                raise forms.ValidationError('쿠폰 금액보다 적은 금액은 사용 불가합니다.')

            if gift_coupon_obj.expire_date < datetime.now().date():
                raise forms.ValidationError('만료된 쿠폰입니다.')

            if gift_coupon_obj.is_used:
                raise forms.ValidationError('이미 사용된 쿠폰입니다.')

        return gift_coupon

    def save(self):
        order = super(OrderModelForm, self).save(commit=False)

        if self.gift_coupon_obj:
            order.total_price = order.total_price - self.gift_coupon_obj.price
            self.gift_coupon_obj.is_used = True
            self.gift_coupon_obj.save()

        order.save()
        return order
