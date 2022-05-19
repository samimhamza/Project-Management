# Generated by Django 4.0.4 on 2022-05-18 10:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0004_user_profile'),
        ('tasks', '0008_delete_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='task_users',
            field=models.ManyToManyField(through='tasks.UserTask', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='usertask',
            name='task',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='users', to='tasks.task'),
        ),
        migrations.AlterField(
            model_name='usertask',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tasks', to=settings.AUTH_USER_MODEL),
        ),
    ]
