# Generated by Django 4.0.4 on 2022-07-13 10:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0007_alter_client_hear_about_us'),
    ]

    operations = [
        migrations.AlterField(
            model_name='priceplan',
            name='feature',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='price_plans', to='clients.feature'),
        ),
    ]
