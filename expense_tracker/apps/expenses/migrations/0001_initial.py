# Generated by Django 5.1.5 on 2025-02-18 19:56

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vendor_name', models.CharField(max_length=255)),
                ('due_day_of_month', models.PositiveIntegerField(default=1)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('last_update_date', models.DateTimeField(auto_now=True)),
                ('date_paid', models.DateField(blank=True, null=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('frequency', models.CharField(choices=[('Monthly', 'Monthly'), ('Quarterly', 'Quarterly'), ('Yearly', 'Yearly')], default='Monthly', max_length=10)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
