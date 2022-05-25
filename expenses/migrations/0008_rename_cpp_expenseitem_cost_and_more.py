# Generated by Django 4.0.4 on 2022-05-25 07:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('expenses', '0007_expense_date_alter_expense_body_alter_expense_type'),
    ]

    operations = [
        migrations.RenameField(
            model_name='expenseitem',
            old_name='cpp',
            new_name='cost',
        ),
        migrations.RenameField(
            model_name='expenseitem',
            old_name='item',
            new_name='name',
        ),
        migrations.AlterField(
            model_name='expenseitem',
            name='expense',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='items', to='expenses.expense'),
        ),
    ]
