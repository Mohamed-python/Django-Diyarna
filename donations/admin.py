from django.contrib import admin
from .models import Case, Donation

# Register your models here.
admin.site.register(Case)
# admin.site.register(Donation)


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):

    exclude = ('name',)

    readonly_fields = (
        'case',
        # 'name', 
        'donor_name',
        'amount', 
        'payment_method', 
        'created_at',
        'is_paid', 
        )


