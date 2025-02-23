# apps/expenses/utils.py
from django.http import HttpResponse
import pandas as pd
from .models import Expense


def import_expenses_from_excel(file, usr):
    try:
        # Read the Excel file
        df = pd.read_excel(file)
        print(f"Excel file loaded with {len(df)} rows.")  # ✅ Debug

        # Mapping Excel column names to database fields
        column_mapping = {
            'Vendor Name': 'vendor_name',
            'Due Date': 'due_date',  # Updated to Due Date for combined month/day
            'Amount': 'amount',
            'Date Paid': 'date_paid',
            'Frequency': 'frequency'
        }

        # Rename columns to match the database model fields
        df.rename(columns=column_mapping, inplace=True)
        print(f"Renamed columns: {df.columns.tolist()}")  # ✅ Debug

        # Validate required columns
        required_columns = ['vendor_name', 'due_date', 'amount', 'frequency']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            print(f"Missing required columns: {missing_columns}")  # ✅ Debug
            return HttpResponse(f"Missing required columns: {', '.join(missing_columns)}", status=400)

        # Process each row in the Excel file
        for index, row in df.iterrows():
            print(f"Processing row {index + 1}: {row.to_dict()}")  # ✅ Debug

            # Handle date fields
            date_paid = pd.to_datetime(row.get('date_paid'), errors='coerce')
            due_date_str = str(row.get('due_date', '')).strip()
            frequency = row.get('frequency', 'Monthly')

            # Parse due_date based on frequency
            if pd.isna(due_date_str) or due_date_str == '':
                print(f"Skipping row {index + 1} due to missing due_date.")  # ✅ Debug
                continue

            if frequency == 'Monthly':
                # Expect just a day number (e.g., "15")
                try:
                    due_day_of_month = int(due_date_str)
                    due_month = None
                except ValueError:
                    print(f"Invalid due_date '{due_date_str}' for Monthly in row {index + 1}, skipping.")  # ✅ Debug
                    continue
            else:  # Quarterly or Yearly
                # Expect "Month Day" format (e.g., "March 15")
                try:
                    month_name, day = due_date_str.split()
                    due_day_of_month = int(day)
                    due_month = {v: k for k, v in Expense.MONTH_CHOICES}.get(month_name.capitalize())
                    if due_month is None:
                        raise ValueError(f"Invalid month name: {month_name}")
                except (ValueError, AttributeError) as e:
                    print(f"Invalid due_date '{due_date_str}' for {frequency} in row {index + 1}, skipping: {e}")  # ✅ Debug
                    continue

            # Validate critical data
            if pd.isna(row.get('vendor_name')) or pd.isna(row.get('amount')):
                print(f"Skipping row {index + 1} due to missing critical data.")  # ✅ Debug
                continue

            # Check for existing expense to avoid duplication
            existing_expense = Expense.objects.filter(
                vendor_name=row['vendor_name'],
                user=usr
            ).first()

            if existing_expense:
                print(f"Duplicate found for vendor '{row['vendor_name']}', skipping.")  # ✅ Debug
                continue

            # Create Expense
            expense = Expense.objects.create(
                vendor_name=row['vendor_name'],
                due_day_of_month=due_day_of_month,
                due_month=due_month,
                amount=row['amount'],
                date_paid=date_paid if not pd.isna(date_paid) else None,
                frequency=frequency,
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
            'Due Date': (
                str(expense.due_day_of_month) if expense.frequency == 'Monthly'
                else f"{dict(Expense.MONTH_CHOICES).get(expense.due_month, 'Unknown')} {expense.due_day_of_month}"
            ),
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
