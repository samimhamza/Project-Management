# Generated by Django 4.0.4 on 2022-05-22 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0010_alter_usertask_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='a_end_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='a_start_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='p_end_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='p_start_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
