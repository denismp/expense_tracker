# # expenses/forms.py
# from django import forms
# from .models import Expense


# class ExpenseForm(forms.ModelForm):
#     class Meta:
#         model = Expense
#         fields = ['vendor_name', 'due_day_of_month', 'amount', 'date_paid', 'frequency']
#         widgets = {
#             'vendor_name': forms.TextInput(attrs={'class': 'form-control'}),
#             'due_day_of_month': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
#             'amount': forms.NumberInput(attrs={'class': 'form-control'}),
#             'date_paid': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
#             'frequency': forms.Select(attrs={'class': 'form-control'}),
#         }

from django import forms
from .models import Expense


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['vendor_name', 'due_day_of_month', 'amount', 'date_paid', 'frequency']
        widgets = {
            'vendor_name': forms.TextInput(attrs={'class': 'form-control'}),
            'due_day_of_month': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 31, 'value': 1}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'date_paid': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'frequency': forms.Select(attrs={'class': 'form-control'}),
        }
