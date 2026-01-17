from django import forms
from .models import Donation

class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ['name', 'amount']

        labels = {
            'name': 'اسم المتبرع',
            'amount': 'مبلغ التبرع',
        }

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'اكتب اسمك'
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'مبلغ التبرع بالجنيه',
                'min': '1'
            }),
        }