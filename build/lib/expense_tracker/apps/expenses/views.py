# apps/expenses/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Expense
from .forms import ExpenseForm
from .utils import import_expenses_from_excel, export_expenses_to_excel


@login_required
def expense_list(request):
    # Get sorting parameters from the request
    sort_by = request.GET.get('sort', 'vendor_name')  # Default sort field
    sort_order = request.GET.get('order', 'asc')

    # Determine sorting direction
    if sort_order == 'desc':
        sort_by = f'-{sort_by}'

    # Retrieve expenses and apply sorting
    expenses = Expense.objects.filter(user=request.user).order_by(sort_by)

    # Format due date for display
    for expense in expenses:
        if expense.frequency == 'Monthly':
            expense.display_due_date = str(expense.due_day_of_month)  # e.g., "15"
        else:  # Quarterly or Yearly
            month_name = dict(Expense.MONTH_CHOICES).get(expense.due_month, 'Unknown')
            expense.display_due_date = f"{month_name} {expense.due_day_of_month}"  # e.g., "March 15"

    # Calculate totals based on frequency
    total_monthly = sum(exp.amount for exp in expenses if exp.frequency == "Monthly")
    total_quarterly = sum(exp.amount for exp in expenses if exp.frequency == "Quarterly")
    total_yearly = sum(exp.amount for exp in expenses if exp.frequency == "Yearly")
    grand_total = total_monthly + total_quarterly + total_yearly

    return render(request, 'expenses/expense_list.html', {
        'expenses': expenses,
        'grand_total': grand_total,
        'total_monthly': total_monthly,
        'total_quarterly': total_quarterly,
        'total_yearly': total_yearly,
        'current_sort': request.GET.get('sort', 'vendor_name'),
        'current_order': request.GET.get('order', 'asc'),
    })


@login_required
def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            # Ensure due_month is None for Monthly expenses
            if expense.frequency == 'Monthly':
                expense.due_month = None
            elif not expense.due_month:  # Validate Quarterly/Yearly
                form.add_error('due_month', 'Month is required for Quarterly or Yearly expenses.')
                return render(request, 'expenses/expense_form.html', {'form': form})
            expense.save()
            return redirect('expenses:expense_list')
    else:
        form = ExpenseForm()
    return render(request, 'expenses/expense_form.html', {'form': form})


@login_required
def edit_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            expense = form.save(commit=False)
            # Ensure due_month is None for Monthly expenses
            if expense.frequency == 'Monthly':
                expense.due_month = None
            elif not expense.due_month:
                form.add_error('due_month', 'Month is required for Quarterly or Yearly expenses.')
                return render(request, 'expenses/expense_form.html', {'form': form})
            expense.save()
            return redirect('expenses:expense_list')
    else:
        form = ExpenseForm(instance=expense)
    return render(request, 'expenses/expense_form.html', {'form': form})


# Other views (expense_detail, delete_expense, import_expenses, export_expenses) unchanged
@login_required
def expense_detail(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    return render(request, 'expenses/expense_detail.html', {'expense': expense})


@login_required
def delete_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    if request.method == 'POST':
        expense.delete()
        return redirect('expenses:expense_list')
    return render(request, 'expenses/confirm_delete.html', {'expense': expense})


@login_required
def import_expenses(request):
    if request.method == 'POST' and request.FILES.get('file'):
        file = request.FILES['file']
        import_expenses_from_excel(file, request.user)
        return redirect('expenses:expense_list')
    return render(request, 'expenses/import_expenses.html')


@login_required
def export_expenses(request):
    file_path = export_expenses_to_excel(request.user)
    with open(file_path, 'rb') as file:
        response = HttpResponse(
            file.read(),
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response["Content-Disposition"] = 'attachment; filename="expenses.xlsx"'
        return response
