from django.db import models
from django.core.validators import MinLengthValidator, RegexValidator

# Create your models here.
class Volunteer(models.Model):

    name = models.CharField(max_length=200, verbose_name="الاسم",
                            validators=[
                                MinLengthValidator(3, message="الاسم يجب أن يكون على الأقل 3 أحرف")
                            ]
        )
    email = models.EmailField(
            verbose_name="البريد الإلكتروني",
            max_length=50,
            error_messages={
            'invalid': "الرجاء إدخال بريد إلكتروني صالح",
            'blank': "البريد الإلكتروني مطلوب"
        }
    )    
    phone = models.CharField(max_length=20, verbose_name="رقم الهاتف", null=True, blank=True)

    VOLUNTEER_TYPE_CHOICES = (
        ('individual', 'فرد'),
        ('group', 'مجموعة'),
    )
    volunteer_type = models.CharField(
        max_length=10,
        choices=VOLUNTEER_TYPE_CHOICES,
        default='individual',
        verbose_name="نوع التطوع"
    )

    group_size = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="عدد أعضاء المجموعة",
        help_text="اكتب عدد أعضاء المجموعة إذا كان التطوع جماعي"
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ التسجيل")

    def save(self, *args, **kwargs):
        if self.volunteer_type == 'individual':
            self.group_size = None
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({'مجموعة' if self.volunteer_type=='group' else 'فرد'})"
