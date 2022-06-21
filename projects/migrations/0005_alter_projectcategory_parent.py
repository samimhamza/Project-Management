# Generated by Django 4.0.4 on 2022-06-21 12:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0004_alter_project_progress'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectcategory',
            name='parent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='project_category', to='projects.projectcategory'),
        ),
    ]
