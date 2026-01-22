from django.contrib import admin

# Register your models here.
from .models import Product, ProductOrder

admin.site.register(Product)
admin.site.register(ProductOrder)



