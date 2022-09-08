# Generated by Django 4.0.4 on 2022-09-08 05:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projects', '0003_remove_projectpermission_users_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectPermissionUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project_permissions', to='projects.project')),
            ],
        ),
        migrations.AddField(
            model_name='projectpermission',
            name='users',
            field=models.ManyToManyField(related_name='project_permission_user', through='projects.ProjectPermissionUser', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='projectpermissionuser',
            name='project_permission',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='project_permission', to='projects.projectpermission'),
        ),
        migrations.AddField(
            model_name='projectpermissionuser',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='project_user_permissions', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='projectpermissionuser',
            unique_together={('project_permission', 'user', 'project')},
        ),
    ]