# Generated by Django 4.0.4 on 2022-09-10 05:08

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='role',
            name='users',
            field=models.ManyToManyField(blank=True, related_name='roles_users', to=settings.AUTH_USER_MODEL),
        ),
    ]
