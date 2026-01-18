from django.db import models
import uuid
from django.utils.text import slugify



def image_upload(instance, filename):
    ext = filename.split('.')[-1]
    return f"cases/{uuid.uuid4()}.{ext}"



# Create your models here.
class News(models.Model):
    title = models.CharField(max_length=200, verbose_name="عنوان الخبر")
    content = models.TextField(verbose_name="محتوى الخبر")
    image = models.ImageField(upload_to=image_upload, verbose_name="صورة الخبر", blank=True, null=True)
    published_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ النشر")
    
    slug = models.SlugField(
        blank=True,
        null=True,
        allow_unicode=True,
        verbose_name="الرابط النصي"
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            # توليد slug من العنوان بالعربي
            self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title