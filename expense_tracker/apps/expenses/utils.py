# apps/expenses/utils.py
import pandas as pd
from io import BytesIO
from .models import Expense


def import_expenses_from_excel(file, usr):
    # Read the Excel file directly from the uploaded file (user's local computer)
    df = pd.read_excel(file)
    print(f"Excel file loaded with {len(df)} rows.")  # ✅ Debug

    # Mapping Excel column names to database fields
    column_mapping = {
        'Vendor Name': 'vendor_name',
        'Due Date': 'due_date',
        'Amount': 'amount',
        'Date Paid': 'date_paid',
        'Frequency': 'frequency'
    }

    # Rename columns to match the database model fields
    df.rename(columns=column_mapping, inplace=True)
    print(f"Renamed columns: {df.columns.to_list()}")  # ✅ Debug

    # Validate required columns
    required_columns = ['vendor_name', 'due_date', 'amount', 'frequency']
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        print(f"Missing required columns: {missing_columns}")  # ✅ Debug
        raise ValueError(f"Missing required columns: {', '.join(missing_columns)}")

    # Process each row in the Excel file
    for index, row in df.iterrows():
        print(f"Processing row {index + 1}: {row.to_dict()}")  # ✅ Debug

        # Handle date fields
        date_paid = pd.to_datetime(row.get('date_paid'), errors='coerce')
        due_date_str = str(row.get('due_date', '')).strip()
        frequency = row.get('frequency', 'Monthly')

        # Parse due_date to get day of month, handling both number and "Month Day" format
        if pd.isna(due_date_str) or due_date_str == '':
            print(f"Skipping row {index + 1} due to missing due_date.")  # ✅ Debug
            continue

        try:
            due_day_of_month = int(due_date_str)
        except ValueError:
            try:
                month_name, day_str = due_date_str.split()
                due_day_of_month = int(day_str)
            except (ValueError, AttributeError):
                print(f"Invalid due_date '{due_date_str}' in row {index + 1}, skipping.")
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

        # Create Expense without due_month
        expense = Expense.objects.create(
            vendor_name=row['vendor_name'],
            due_day_of_month=due_day_of_month,
            amount=row['amount'],
            date_paid=date_paid if not pd.isna(date_paid) else None,
            frequency=frequency,
            user=usr
        )
        print(f"Successfully added expense: {expense.vendor_name}")  # ✅ Debug


def export_expenses_to_excel(user):
    # Retrieve expenses for the user
    expenses = Expense.objects.filter(user=user)
    data = [
        {
            'Vendor Name': expense.vendor_name,
            'Due Date': str(expense.due_day_of_month),
            'Amount': expense.amount,
            'Date Paid': expense.date_paid,
            'Frequency': expense.frequency,
        }
        for expense in expenses
    ]
    df = pd.DataFrame(data)

    # Generate the Excel file in memory instead of writing to the server
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False)
    output.seek(0)  # Rewind the buffer to the beginning

    return output  # Return the in-memory file
