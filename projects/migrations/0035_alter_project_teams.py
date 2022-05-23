# Generated by Django 4.0.4 on 2022-05-23 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_alter_team_users'),
        ('projects', '0034_alter_project_teams'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='teams',
            field=models.ManyToManyField(related_name='%(class)ss', to='users.team'),
        ),
    ]
