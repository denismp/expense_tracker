# expenses/forms.py
from django import forms
from .models import Expense


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['vendor_name', 'due_date', 'amount', 'date_paid', 'frequency']
        widgets = {
            'vendor_name': forms.TextInput(attrs={'class': 'form-control'}),
            'due_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'date_paid': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'frequency': forms.Select(attrs={'class': 'form-control'}),
        }
