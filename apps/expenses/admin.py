# Register your models here.
# expenses/admin.py
from django.contrib import admin
from .models import Expense


class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('vendor_name', 'due_day_of_month', 'amount', 'date_paid', 'frequency', 'user')
    list_filter = ('due_day_of_month', 'date_paid', 'user', 'frequency')
    search_fields = ('vendor_name', 'user__username', 'frequency')
    ordering = ('-due_day_of_month',)


admin.site.register(Expense, ExpenseAdmin)
