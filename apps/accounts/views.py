# from django.shortcuts import render

# Create your views here.
# accounts/views.py
from django.shortcuts import render, redirect
# from django.contrib.auth import login, authenticate, logout
from django.contrib.auth import login
from .forms import CustomUserCreationForm


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('expenses:expense_list')  # ✅ Use namespaced URL
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})
