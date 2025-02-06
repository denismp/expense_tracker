# expenses/forms.py
from django import forms
from .models import Expense


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['vendor_name', 'due_date', 'amount', 'date_paid']
