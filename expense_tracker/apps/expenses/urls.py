from django.urls import path
from . import views

app_name = "expenses"  # ✅ Namespacing added

urlpatterns = [
    path('', views.expense_list, name='expense_list'),
    path('add/', views.add_expense, name='add_expense'),
    path('<int:pk>/', views.expense_detail, name='expense_detail'),
    path('edit/<int:pk>/', views.edit_expense, name='edit_expense'),
    path('delete/<int:pk>/', views.delete_expense, name='delete_expense'),
    path('import/', views.import_expenses, name='import_expenses'),
    path('export/', views.export_expenses, name='export_expenses'),
]
