from django.db import models

# Create your models here.
class Order(models.Model):
    STATUS_CHOICES = (
        ("PENDING", "Pending"),
        ("PAID", "Paid"),
        ("FAILED", "Failed"),
    )

    merchant_order_id = models.CharField(max_length=100, unique=True)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    cart_data = models.JSONField()
    # transaction_id = models.CharField(max_length=150, blank=True, null=True)
    payment_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{str(self.amount)} - {self.payment_status}"
