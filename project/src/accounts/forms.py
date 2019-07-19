from django import forms
from accounts.models import User


class MyPageForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('phone', 'address', 'address_detail')


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email',)
