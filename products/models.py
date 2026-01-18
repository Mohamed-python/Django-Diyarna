from django.db import models
import uuid


def image_upload(instance, filename):
    ext = filename.split('.')[-1]
    return f"products/{uuid.uuid4()}.{ext}"


# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to=image_upload)  # الصورة هتتحفظ في media/products/
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)  # التاريخ تلقائي

    def __str__(self):
        return self.name
