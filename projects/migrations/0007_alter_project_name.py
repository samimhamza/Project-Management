# Generated by Django 4.0.4 on 2022-07-31 07:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0006_alter_project_a_end_date_alter_project_a_start_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='name',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
    ]
