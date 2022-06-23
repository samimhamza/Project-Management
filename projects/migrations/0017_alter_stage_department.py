# Generated by Django 4.0.4 on 2022-06-23 09:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0016_rename_departments_stage_department'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stage',
            name='department',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='department_stage', to='projects.department'),
        ),
    ]
