# Generated by Django 4.0.4 on 2022-07-04 09:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0003_income_date_payment_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='income',
            name='date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='payment',
            name='date',
            field=models.DateField(),
        ),
    ]
