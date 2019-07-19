from django import forms


class YosigyTicketForm(forms.Form):
    menu_id = forms.CharField(label='메뉴 ID', max_length=100)
    quantity = forms.IntegerField(label='메뉴 개수')
    discounted_price = forms.IntegerField(label='메뉴 가격')

    def clean_discounted_price(self):
        discounted_price = self.cleaned_data.get('discounted_price')
        if discounted_price < 0:
            raise forms.ValidationError('가격은 0원 이상 입니다.')
        return discounted_price

    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if quantity < 1 or quantity > 100:
            raise forms.ValidationError('개수는 1~100 개 까지 입력 가능합니다.')
        return quantity
