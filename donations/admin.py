from django.contrib import admin
from .models import Case, Donation
# from django.apps import AppConfig

# Register your models here.
@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
    exclude = ('slug','views_count')
    # readonly_fields = (
    #     )

###############################
@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    exclude = ('case',)
    readonly_fields = (
        # 'case',
        'name', 
        'donor_name',
        'amount', 
        'payment_method', 
        'created_at',
        'is_paid', 
        )


