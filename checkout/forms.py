from django.forms import ModelForm
from django import forms
from .models import Order

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['full_name', 'email', 'phone_number',]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            'full_name':'Enter your full name ',
            'email':'Email',
            'phone_number':'Enter your phone number',
        }
        for field in self.fields:
            if self.fields[field].required:
                self.fields[field].widget.attrs['placeholder'] = f' {placeholders[field]} *'
            else:
                self.fields[field].widget.attrs['placeholder'] = placeholders[field]
            self.fields[field].widget.attrs['class'] = 'form-control'
            self.fields[field].label = False
