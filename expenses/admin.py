# Register your models here.
# expenses/admin.py
from django.contrib import admin
from .models import Expense


class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('vendor_name', 'due_date', 'amount', 'date_paid', 'frequency', 'user')
    list_filter = ('due_date', 'date_paid', 'user', 'frequency')
    search_fields = ('vendor_name', 'user__username', 'frequency')
    ordering = ('-due_date',)


admin.site.register(Expense, ExpenseAdmin)
