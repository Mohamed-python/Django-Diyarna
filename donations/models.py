from django.db import models

# Create your models here.
def image_upload(instance, file_name):
    imagename, extension = file_name.split(".")
    return f"cases/{instance.id}.{extension}"



# اضافه حاله
class Case(models.Model):
    title = models.CharField(max_length=200, verbose_name="عنوان الحالة")
    image = models.ImageField(upload_to=image_upload, verbose_name="صورة الحالة")
    description = models.TextField(verbose_name="الوصف")
    goal = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="الهدف")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    # لحساب مجموع التبرعات للحالة (اختياري)
    def total_donations(self):
        return sum(d.amount for d in self.donations.all())

    # لحساب نسبة الإنجاز
    def progress_percent(self):
        if self.goal:
            return (self.total_donations() / self.goal) * 100
        return 0
    



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

    


