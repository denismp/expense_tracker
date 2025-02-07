# Create your models here.
from django.db import models
from django.contrib.auth import get_user_model


class Expense(models.Model):
    FREQUENCY_CHOICES = [
        ('Monthly', 'Monthly'),
        ('Quarterly', 'Quarterly'),
        ('Yearly', 'Yearly'),
    ]

    vendor_name = models.CharField(max_length=255)
    due_date = models.DateField()
    create_date = models.DateTimeField(auto_now_add=True)
    last_update_date = models.DateTimeField(auto_now=True)
    date_paid = models.DateField(null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    # frequency = models.CharField(max_length=10, choices=FREQUENCY_CHOICES, default='Monthly')
    frequency = models.CharField(max_length=10, choices=FREQUENCY_CHOICES, default='Monthly')  # ✅ Choices defined
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
