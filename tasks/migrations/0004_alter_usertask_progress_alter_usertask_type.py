# Generated by Django 4.0.4 on 2022-06-15 07:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0003_task_pin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usertask',
            name='progress',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='usertask',
            name='type',
            field=models.CharField(choices=[('assign', 'Assign'), ('revoke', 'Revoke')], default='assign', max_length=24),
        ),
    ]
