from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False
    )

    class Meta:
        model = Profile
        fields = ['bio', 'phone', 'address', 'gender', 'date_of_birth', 'website', 'image']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3}),
        }

