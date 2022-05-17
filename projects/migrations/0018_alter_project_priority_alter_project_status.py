# Generated by Django 4.0.4 on 2022-05-17 07:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0017_alter_project_priority'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='priority',
            field=models.CharField(choices=[('critical', 'Critical'), ('very_important', 'Very Important'), ('important', 'Important'), ('normal', 'Normal'), ('less_important', 'Less Important')], default='normal', max_length=24),
        ),
        migrations.AlterField(
            model_name='project',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('in_progress', 'In Progress'), ('completed', 'Completed'), ('issue_faced', 'Very Important'), ('failed', 'Failed'), ('cancelled', 'Cancelled')], default='pending', max_length=24),
        ),
    ]
