# Generated by Django 4.0.4 on 2022-08-02 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0017_requirement_target_age'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requirement',
            name='target_audience',
            field=models.JSONField(blank=True, null=True),
        ),
    ]
