from django.db import models
import uuid
from django.contrib.auth.models import User
from django.utils import translation

def image_upload(instance, filename):
    ext = filename.split('.')[-1]
    return f"products/{uuid.uuid4()}.{ext}"


# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=200)
    name_en = models.CharField(max_length=200, blank=True, null=True)
    image = models.ImageField(upload_to=image_upload)  # الصورة هتتحفظ في media/products/
    image_en = models.ImageField(upload_to=image_upload, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    description_en = models.TextField( blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)  # التاريخ تلقائي
    views_count = models.PositiveIntegerField(default=0)
    #################

    def __str__(self):
        lang = translation.get_language()
        if lang == 'en' and self.name_en:
            return self.name_en
        return self.name

    def display_description(self):
        lang = translation.get_language()
        if lang == 'en' and self.description_en:
            return self.description_en
        return self.description
    
    def display_image(self):
        lang = translation.get_language()
        if lang == 'en' and self.image_en:
            return self.image_en
        return self.image





class ProductOrder(models.Model):
    
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name='orders')
    buyer_name = models.CharField(max_length=200)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=200, blank=True, null=True)
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    product_image = models.CharField(max_length=500, blank=True, null=True)  # نخزن رابط الصورة فقط

    def __str__(self):
        return f"{self.product.name if self.product else 'Deleted'}"














