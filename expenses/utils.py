# expenses/utils.py
import pandas as pd
from .models import Expense
# from django.contrib.auth import get_user_model


def import_expenses_from_excel(file, user):
    df = pd.read_excel(file)
    for _, row in df.iterrows():
        Expense.objects.create(
            vendor_name=row['Vendor Name'],
            due_date=row['Due Date'],
            amount=row['Amount'],
            date_paid=row.get('Date Paid', None),
            user=user
        )


def export_expenses_to_excel(user):
    expenses = Expense.objects.filter(user=user)
    data = [
        {
            'Vendor Name': expense.vendor_name,
            'Due Date': expense.due_date,
            'Amount': expense.amount,
            'Date Paid': expense.date_paid,
        }
        for expense in expenses
    ]
    df = pd.DataFrame(data)
    file_path = f'expenses_{user.username}.xlsx'
    df.to_excel(file_path, index=False)
    return file_path
