"""
URL configuration for expense_tracker project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from pathlib import Path
from django.urls import path, include
from django.shortcuts import redirect
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

"""
URL configuration for expense_tracker project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# Define PACKAGE_PREFIX to match settings.py
PACKAGE_PREFIX = 'expense_tracker' if 'site-packages' in str(Path(__file__).resolve().parent.parent) else ''

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('accounts/', include(f'{PACKAGE_PREFIX}.apps.accounts.urls' if PACKAGE_PREFIX else 'apps.accounts.urls')),
    # path('expenses/', include(f'{PACKAGE_PREFIX}.apps.expenses.urls' if PACKAGE_PREFIX else 'apps.expenses.urls')),
    path('accounts/', include('expense_tracker.apps.accounts.urls')),
    path('expenses/', include('expense_tracker.apps.expenses.urls')),
    path('', lambda request: redirect('expenses:expense_list', permanent=False)),
]

# Serve static files in development or frozen mode
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
