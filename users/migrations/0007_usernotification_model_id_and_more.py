# Generated by Django 4.0.4 on 2022-06-15 05:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_usernotification_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='usernotification',
            name='model_id',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='usernotification',
            name='model_name',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
    ]
