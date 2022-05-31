# Generated by Django 4.0.4 on 2022-05-31 05:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0018_action_role_subaction_permission'),
    ]

    operations = [
        migrations.AlterField(
            model_name='action',
            name='codename',
            field=models.CharField(max_length=64, unique=True),
        ),
        migrations.AlterField(
            model_name='action',
            name='name',
            field=models.CharField(max_length=64, unique=True),
        ),
        migrations.AlterField(
            model_name='subaction',
            name='code',
            field=models.CharField(max_length=32, unique=True),
        ),
        migrations.AlterField(
            model_name='subaction',
            name='name',
            field=models.CharField(max_length=64, unique=True),
        ),
    ]
