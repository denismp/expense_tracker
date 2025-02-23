# apps/expenses/models.py
from django.db import models
from django.contrib.auth import get_user_model


class Expense(models.Model):
    FREQUENCY_CHOICES = [
        ('Monthly', 'Monthly'),
        ('Quarterly', 'Quarterly'),
        ('Yearly', 'Yearly'),
    ]
    MONTH_CHOICES = [
        (1, 'January'),
        (2, 'February'),
        (3, 'March'),
        (4, 'April'),
        (5, 'May'),
        (6, 'June'),
        (7, 'July'),
        (8, 'August'),
        (9, 'September'),
        (10, 'October'),
        (11, 'November'),
        (12, 'December'),
    ]

    vendor_name = models.CharField(max_length=255)
    due_day_of_month = models.PositiveIntegerField(default=1)
    due_month = models.PositiveIntegerField(choices=MONTH_CHOICES, null=True, blank=True)  # New field for quarterly/yearly
    create_date = models.DateTimeField(auto_now_add=True)
    last_update_date = models.DateTimeField(auto_now=True)
    date_paid = models.DateField(null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    frequency = models.CharField(
        max_length=10,
        choices=FREQUENCY_CHOICES,
        default='Monthly'
    )
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        if self.frequency == 'Monthly':
            return f"{self.vendor_name} - Due on day {self.due_day_of_month}"
        else:
            month_name = dict(self.MONTH_CHOICES).get(self.due_month, 'Unknown')
            return f"{self.vendor_name} - Due on {month_name} {self.due_day_of_month}"
