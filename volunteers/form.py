from django import forms
from .models import Volunteer

class VolunteerForm(forms.ModelForm):
    name = forms.CharField(
        label="الاسم",
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'الاسم'}),
        error_messages={
            'required': 'الاسم مطلوب',
            'min_length': 'الاسم يجب أن يكون على الأقل 3 أحرف'
        },
        min_length=3
    )

    email = forms.EmailField(
        label="البريد الإلكتروني",
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'البريد الإلكتروني'}),
        error_messages={
            'required': 'البريد الإلكتروني مطلوب',
            'invalid': 'الرجاء إدخال بريد إلكتروني صالح'
        }
    )

    phone = forms.CharField(
        label="رقم الهاتف",
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'رقم الهاتف'}),
        error_messages={
            'required': 'رقم الهاتف مطلوب'
        }
    )

    class Meta:
        model = Volunteer
        fields = ['name', 'email', 'phone', 'volunteer_type', 'group_size']
        widgets = {
            'volunteer_type': forms.Select(attrs={'class': 'form-select', 'id': 'id_volunteer_type'}),
            'group_size': forms.NumberInput(attrs={'class': 'form-control', 'id': 'id_group_size', 'min':1}),
        }
        labels = {
            'volunteer_type': 'نوع التطوع',
            'group_size': 'عدد أعضاء المجموعة',
        }

    # فلديشن رقم الهاتف
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not phone.isdigit():
            raise forms.ValidationError("رقم الهاتف يجب أن يحتوي على أرقام فقط")
        if len(phone) < 8 or len(phone) > 15:
            raise forms.ValidationError("رقم الهاتف يجب أن يكون بين 8 و15 رقم")
        return phone

    # فلديشن عدد أعضاء المجموعة
    def clean_group_size(self):
        volunteer_type = self.cleaned_data.get('volunteer_type')
        group_size = self.cleaned_data.get('group_size')
        if volunteer_type == 'group':
            if group_size is None or group_size < 1:
                raise forms.ValidationError("يرجى إدخال عدد أعضاء المجموعة بشكل صحيح")
        return group_size
