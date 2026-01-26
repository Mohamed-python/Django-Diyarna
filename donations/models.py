from django.db import models
import uuid
from django.utils.text import slugify
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

# Create your models here.
def image_upload(instance, filename):
    ext = filename.split('.')[-1]
    return f"cases/{uuid.uuid4()}.{ext}"



# اضافه حاله
class Case(models.Model):
    title = models.CharField(max_length=200, verbose_name="عنوان الحالة")
    description = models.TextField(verbose_name="الوصف")
    goal = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="الهدف")
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(max_length=200,upload_to=image_upload, verbose_name="صورة الحالة")
    slug = models.SlugField(blank=True, null=True, verbose_name="الرابط النصي من العنوان")
    views_count = models.PositiveIntegerField(default=0)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)



    def __str__(self):
        return self.title

    # لحساب مجموع التبرعات للحالة (اختياري)
    def total_donations(self):
        return sum(d.amount for d in self.donations.all())

    def progress_percent(self):
        if not self.goal:
            return 0
        percent = (self.total_donations() / self.goal) * 100
        return min(round(percent, 2), 100)

    def progress_text(self):
        return f"{self.total_donations()} / {self.goal}"
    

# نموذج التبرعات
class Donation(models.Model):
    PAYMENT_CHOICES = [
        ('cash', 'كاش'),
        ('visa', 'فيزا'),
        ('vodafone', 'فودافون كاش'),
    ]
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='donations')
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_CHOICES,
        blank=True,
        null=True
    )
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.amount}"

