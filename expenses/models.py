# Create your models here.
from django.db import models
from django.contrib.auth import get_user_model


class Expense(models.Model):
    vendor_name = models.CharField(max_length=255)
    due_date = models.DateField()
    create_date = models.DateTimeField(auto_now_add=True)
    last_update_date = models.DateTimeField(auto_now=True)
    date_paid = models.DateField(null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
