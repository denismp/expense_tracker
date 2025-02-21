# expenses/utils.py
from django.http import HttpResponse
import pandas as pd
from .models import Expense


# def import_expenses_from_excel(file, usr):
#     try:
#         # Read the Excel file
#         df = pd.read_excel(file)
#         print(f"Excel file loaded with {len(df)} rows.")  # ✅ Debug

#         # Mapping Excel column names to database fields
#         column_mapping = {
#             'Vendor Name': 'vendor_name',
#             'Due Day Of Month': 'due_day_of_month',
#             'Amount': 'amount',
#             'Date Paid': 'date_paid',
#             'Frequency': 'frequency'
#         }

#         # Rename columns to match the database model fields
#         df.rename(columns=column_mapping, inplace=True)
#         print(f"Renamed columns: {df.columns.tolist()}")  # ✅ Debug

#         # Validate required columns
#         required_columns = ['vendor_name', 'due_day_of_month', 'amount']
#         missing_columns = [col for col in required_columns if col not in df.columns]
#         if missing_columns:
#             print(f"Missing required columns: {missing_columns}")  # ✅ Debug
#             return HttpResponse(f"Missing required columns: {', '.join(missing_columns)}", status=400)

#         # Process each row in the Excel file
#         for index, row in df.iterrows():
#             print(f"Processing row {index + 1}: {row.to_dict()}")  # ✅ Debug

#             # Handle NaT or NaN for date fields
#             due_day_of_month = pd.to_datetime(row.get('due_day_of_month'), errors='coerce')
#             date_paid = pd.to_datetime(row.get('date_paid'), errors='coerce')

#             # Validate data before creating the expense
#             if pd.isna(row.get('vendor_name')) or pd.isna(due_day_of_month) or pd.isna(row.get('amount')):
#                 print(f"Skipping row {index + 1} due to missing critical data.")  # ✅ Debug
#                 continue  # Skip rows with missing critical data

#             # Check for existing expense to avoid duplication based on vendor_name
#             existing_expense = Expense.objects.filter(
#                 vendor_name=row['vendor_name'],
#                 user=usr
#             ).first()

#             if existing_expense:
#                 print(f"Duplicate found for vendor '{row['vendor_name']}', skipping.")  # ✅ Debug
#                 continue  # Skip if duplicate found

#             # Create Expense if not a duplicate
#             expense = Expense.objects.create(
#                 vendor_name=row['vendor_name'],
#                 due_day_of_month=due_day_of_month if not pd.isna(due_day_of_month) else None,
#                 amount=row['amount'],
#                 date_paid=date_paid if not pd.isna(date_paid) else None,
#                 frequency=row.get('frequency', 'Monthly'),  # Default to 'Monthly' if missing
#                 user=usr
#             )
#             print(f"Successfully added expense: {expense.vendor_name}")  # ✅ Debug

#         return HttpResponse("Expenses imported successfully.", status=200)

#     except Exception as e:
#         print(f"Error occurred: {e}")  # ✅ Debug
#         return HttpResponse(f"Error processing the file: {str(e)}", status=500)

def import_expenses_from_excel(file, usr):
    try:
        # Read the Excel file
        df = pd.read_excel(file)
        print(f"Excel file loaded with {len(df)} rows.")  # ✅ Debug

        # Mapping Excel column names to database fields
        column_mapping = {
            'Vendor Name': 'vendor_name',
            'Due Day Of Month': 'due_day_of_month',
            'Amount': 'amount',
            'Date Paid': 'date_paid',
            'Frequency': 'frequency'
        }

        # Rename columns to match the database model fields
        df.rename(columns=column_mapping, inplace=True)
        print(f"Renamed columns: {df.columns.tolist()}")  # ✅ Debug

        # Validate required columns
        required_columns = ['vendor_name', 'due_day_of_month', 'amount']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            print(f"Missing required columns: {missing_columns}")  # ✅ Debug
            return HttpResponse(f"Missing required columns: {', '.join(missing_columns)}", status=400)

        # Ensure due_day_of_month is an integer (Extract day if mistakenly stored as a date)
        df['due_day_of_month'] = pd.to_numeric(df['due_day_of_month'], errors='coerce').fillna(1).astype(int)

        # Process each row in the Excel file
        for index, row in df.iterrows():
            print(f"Processing row {index + 1}: {row.to_dict()}")  # ✅ Debug

            # Handle NaN values for date fields
            date_paid = pd.to_datetime(row.get('date_paid'), errors='coerce')
            due_day_of_month = row['due_day_of_month']  # ✅ Now guaranteed to be an integer

            # Validate critical data before creating the expense
            if pd.isna(row.get('vendor_name')) or pd.isna(due_day_of_month) or pd.isna(row.get('amount')):
                print(f"Skipping row {index + 1} due to missing critical data.")  # ✅ Debug
                continue  # Skip rows with missing critical data

            # Check for existing expense to avoid duplication based on vendor_name
            existing_expense = Expense.objects.filter(
                vendor_name=row['vendor_name'],
                user=usr
            ).first()

            if existing_expense:
                print(f"Duplicate found for vendor '{row['vendor_name']}', skipping.")  # ✅ Debug
                continue  # Skip if duplicate found

            # Create Expense if not a duplicate
            expense = Expense.objects.create(
                vendor_name=row['vendor_name'],
                due_day_of_month=due_day_of_month,  # ✅ Ensured integer
                amount=row['amount'],
                date_paid=date_paid if not pd.isna(date_paid) else None,
                frequency=row.get('frequency', 'Monthly'),  # Default to 'Monthly' if missing
                user=usr
            )
            print(f"Successfully added expense: {expense.vendor_name}")  # ✅ Debug

        return HttpResponse("Expenses imported successfully.", status=200)

    except Exception as e:
        print(f"Error occurred: {e}")  # ✅ Debug
        return HttpResponse(f"Error processing the file: {str(e)}", status=500)


def export_expenses_to_excel(user):
    expenses = Expense.objects.filter(user=user)
    data = [
        {
            'Vendor Name': expense.vendor_name,
            'Due Day Of Month': expense.due_day_of_month,
            'Amount': expense.amount,
            'Date Paid': expense.date_paid,
            'Frequency': expense.frequency,
        }
        for expense in expenses
    ]
    df = pd.DataFrame(data)
    file_path = f'expenses_{user.username}.xlsx'
    df.to_excel(file_path, index=False)
    return file_path
