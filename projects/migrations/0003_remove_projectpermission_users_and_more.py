# Generated by Django 4.0.4 on 2022-09-08 05:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='projectpermission',
            name='users',
        ),
        migrations.DeleteModel(
            name='ProjectPermissionUser',
        ),
    ]
