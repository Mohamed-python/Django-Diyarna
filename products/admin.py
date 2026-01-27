from django.contrib import admin

# Register your models here.
from .models import Product, ProductOrder

admin.site.register(Product)
@admin.register(ProductOrder)
class ProductOrderAdmin(admin.ModelAdmin):

    # exclude = ('payment_method',)

    readonly_fields = (
        'payment_method', 
        'product',
        'buyer_name', 
        'quantity', 
        'total_price', 
        'created_at',
        'product_image',
        'is_paid',
        )



