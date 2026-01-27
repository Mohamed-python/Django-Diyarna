from django.db import models
import uuid
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.utils import translation



def image_upload(instance, filename):
    ext = filename.split('.')[-1]
    return f"news/{uuid.uuid4()}.{ext}"



# Create your models here.
class News(models.Model):
    title = models.CharField(max_length=200, verbose_name="عنوان الخبر")
    title_en = models.CharField(max_length=200, verbose_name="News title English", blank=True, null=True)

    content = models.TextField(verbose_name="محتوى الخبر")
    content_en = models.TextField(verbose_name="Content In English", blank=True, null=True)

    image = models.ImageField(upload_to=image_upload, verbose_name="صورة الخبر", blank=True, null=True)
    image_en = models.ImageField(upload_to=image_upload, verbose_name="News Picture English", blank=True, null=True)
    views_count = models.PositiveIntegerField(default=0)

    published_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ النشر")
    
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='news_posts',
        verbose_name="الناشر"
    )
    slug = models.SlugField(blank=True, null=True, allow_unicode=True, verbose_name="الرابط النصي")
    slug_en = models.SlugField(blank=True, null=True, allow_unicode=True, verbose_name="slug_en")



    class Meta:
        permissions = [
            ("can_publish_news", "Can publish news"),
        ]
    #####################################################################

    def save(self, *args, **kwargs):
        # توليد slug عربي لو مش موجود
        if not self.slug and self.title:
            self.slug = slugify(self.title, allow_unicode=True)
        # توليد slug إنجليزي لو مش موجود
        if not self.slug_en and self.title_en:
            self.slug_en = slugify(self.title_en, allow_unicode=True)
        super().save(*args, **kwargs)

    @property
    def title_by_lang(self):
        lang = translation.get_language()
        if lang == 'ar':
            return self.title if self.title else self.title_en
        return self.title_en if self.title_en else self.title

    @property
    def content_by_lang(self):
        lang = translation.get_language()
        if lang == 'ar':
            return self.content if self.content else self.content_en
        return self.content_en if self.content_en else self.content

    @property
    def slug_by_lang(self):
        lang = translation.get_language()
        if lang == 'ar':
            return self.slug if self.slug else self.slug_en
        return self.slug_en if self.slug_en else self.slug

    @property
    def image_by_lang(self):
        lang = translation.get_language()
        if lang == 'ar':
            return self.image if self.image else self.image_en
        return self.image_en if self.image_en else self.image

    def __str__(self):
        return self.title_by_lang