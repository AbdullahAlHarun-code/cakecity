from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User
from .models import Customer, BillingAddress, ShippingAddress
from django import forms

class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    def clean_email(self):
        data = self.cleaned_data['email']
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError("This email already used")
        return data

class CustomerChangePassword(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'type':'password'}))
    new_password1 = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'class':'form-control', 'type':'password'}))
    new_password2 = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'class':'form-control', 'type':'password'}))
    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']

class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'email', 'phone']

class BillingAddressForm(ModelForm):
    class Meta:
        model = BillingAddress
        fields = ['address_line_1', 'address_line_2', 'address_line_3', 'city', 'eircode']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            'address_line_1':'Address Line 1',
            'address_line_2':'Address Line 2',
            'address_line_3':'Address Line 3',
            'city':'Town or city',
            'eircode':'Post code or eircode',
        }
        for field in self.fields:
            if self.fields[field].required:
                #placeholder = self.fields[field]
                self.fields[field].widget.attrs['placeholder'] = f' {placeholders[field]} *'
            else:
                self.fields[field].widget.attrs['placeholder'] = placeholders[field]
            self.fields[field].widget.attrs['class'] = 'form-control'
            self.fields[field].label = False
#git config --global user.email "you@example.com"
  #git config --global user.name "Your Name"
class ShippingAddressForm(ModelForm):
    class Meta:
        model = ShippingAddress
        fields = ['address_line_1', 'address_line_2', 'address_line_3', 'city', 'eircode']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            'address_line_1':'Address Line 1',
            'address_line_2':'Address Line 2',
            'address_line_3':'Address Line 3',
            'city':'Town or city',
            'eircode':'Post code or eircode',
        }
        for field in self.fields:
            if self.fields[field].required:
                #placeholder = self.fields[field]
                self.fields[field].widget.attrs['placeholder'] = f' {placeholders[field]} *'
            else:
                self.fields[field].widget.attrs['placeholder'] = placeholders[field]
            self.fields[field].widget.attrs['class'] = 'form-control'
            self.fields[field].label = False
