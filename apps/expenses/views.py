# expenses/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Expense
from .forms import ExpenseForm
from .utils import import_expenses_from_excel, export_expenses_to_excel


@login_required
def expense_list(request):
    """ View to list all expenses for the logged-in user """
    expenses = Expense.objects.filter(user=request.user)
    return render(request, 'expenses/expense_list.html', {'expenses': expenses})


@login_required
def add_expense(request):
    """ View to add a new expense """
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            return redirect('expenses:expense_list')  # ✅ Fixed namespace reference
    else:
        form = ExpenseForm()

    return render(request, 'expenses/expense_form.html', {'form': form})  # ✅ Ensure response for GET request


@login_required
def expense_detail(request, pk):
    """ View to display a specific expense detail """
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    return render(request, 'expenses/expense_detail.html', {'expense': expense})


@login_required
def edit_expense(request, pk):
    """ View to edit an existing expense """
    expense = get_object_or_404(Expense, pk=pk, user=request.user)

    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect('expenses:expense_list')  # ✅ Fixed namespace reference
    else:
        form = ExpenseForm(instance=expense)

    return render(request, 'expenses/expense_form.html', {'form': form})


@login_required
def delete_expense(request, pk):
    """ View to delete an expense """
    expense = get_object_or_404(Expense, pk=pk, user=request.user)

    if request.method == 'POST':
        expense.delete()
        return redirect('expenses:expense_list')  # ✅ Fixed namespace reference

    return render(request, 'expenses/confirm_delete.html', {'expense': expense})


@login_required
def import_expenses(request):
    """ View to import expenses from an Excel file """
    if request.method == 'POST' and request.FILES.get('file'):
        file = request.FILES['file']
        import_expenses_from_excel(file, request.user)
        return redirect('expenses:expense_list')  # ✅ Fixed namespace reference

    return render(request, 'expenses/import_expenses.html')


@login_required
def export_expenses(request):
    """ View to export expenses to an Excel file and return as a download """
    file_path = export_expenses_to_excel(request.user)

    with open(file_path, 'rb') as file:
        response = HttpResponse(
            file.read(),
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response["Content-Disposition"] = 'attachment; filename="expenses.xlsx"'
        return response
