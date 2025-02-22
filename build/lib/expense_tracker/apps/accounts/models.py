# from django.contrib.auth.models import AbstractUser
# from django.db import models


# class CustomUser(AbstractUser):
#     force_password_change = models.BooleanField(default=False)

# accounts/models.py
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models


class CustomUser(AbstractUser):
    print("Loading expense_tracker.apps.accounts.models")
    force_password_change = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        Group,
        related_name='customuser_set',  # Custom related name
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_permissions',  # Custom related name
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )
