from .models import Order
from django import forms

class PostForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['order_reference', 'email']
        # exclude = ['created_at', 'user']  # كل الحقول هتكون موجودة ما عدا الحقول دي
        