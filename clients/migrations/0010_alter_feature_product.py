# Generated by Django 4.0.4 on 2022-07-17 12:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0009_remove_feature_created_at_remove_feature_created_by_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feature',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='product_features', to='clients.product'),
        ),
    ]
