from django.contrib import admin
from .models import Order
# Register your models here.
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    # list_display = ('amount', 'created_at')
    # list_filter = ('payment_status', 'created_at')
    # search_fields = ('merchant_order_id', 'email', 'phone')
    # ordering = ('-created_at',)  # ترتيب من الأحدث للأقدم
    # readonly_fields = ('created_at',)  # منع تعديل تاريخ الإنشاء
    exclude = ('amount' ,'payment_status', 'cart_data')
    # fields = ('email','amount')
    readonly_fields = ('amount', 'created_at','payment_status', 'phone', 'email', 'merchant_order_id')