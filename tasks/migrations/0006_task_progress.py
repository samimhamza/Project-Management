# Generated by Django 4.0.4 on 2022-06-18 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0005_alter_usertask_unique_together'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='progress',
            field=models.IntegerField(default=0),
        ),
    ]
