import datetime

from django import forms

from order.models import Order
from yosigy.models import Yosigy, YosigyMenu

YOSIGY_PERIOD_DAYS = 10;


class YosigyForm(forms.ModelForm):
    class Meta:
        model = Yosigy
        fields = (
            'restaurant',
            'user',
            'notice',
            'min_price'
        )

    def clean_restaurant(self):
        restaurant = self.cleaned_data.get('restaurant')
        yosigy_qs = Yosigy.objects.filter(
            deadline__gte=datetime.datetime.now(), restaurant=restaurant)

        if yosigy_qs:
            raise forms.ValidationError('이미 이벤트를 진행 중 입니다.')
        return restaurant

    def save(self):
        yosigy = super(YosigyForm, self).save(commit=False)
        yosigy.deadline = datetime.datetime.now() + datetime.timedelta(days=YOSIGY_PERIOD_DAYS)
        yosigy.save()

        return yosigy


class YosigyMenuForm(forms.ModelForm):
    class Meta:
        model = YosigyMenu
        fields = (
            'discounted_price',
        )


class YosigyOrderModelForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = (
            'user',
            'address',
            'address_detail',
            'phone_num',
            'yosigy_ticket',
            'restaurant',
        )
