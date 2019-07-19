from django import forms

from cart.models import Cart, CartItem


class CartModelForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = ('user',)


class CartItemModelForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = ('cart', 'menu')


class CartItemUpdateModelForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = ('quantity', 'menu')

    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if quantity > 100 or quantity < 1:
            raise forms.ValidationError('quantity의 개수가 올바르지 않습니다.')
        return quantity
