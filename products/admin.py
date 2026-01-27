from django.contrib import admin

# Register your models here.
from .models import Product, Donation

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # list_display = ('donor_name', 'quantity', 'total_price')
    pass
    



@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):

    # exclude = ('payment_method',)

    readonly_fields = (
        'payment_method', 
        'product',
        'donor_name', 
        'quantity', 
        'total_price', 
        'created_at',
        'product_image',
        'is_paid',
        )



