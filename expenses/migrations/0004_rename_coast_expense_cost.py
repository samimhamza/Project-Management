# Generated by Django 4.0.4 on 2022-04-26 07:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('expenses', '0003_category_created_at_category_created_by_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='expense',
            old_name='coast',
            new_name='cost',
        ),
    ]
