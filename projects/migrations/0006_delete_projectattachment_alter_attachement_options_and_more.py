# Generated by Django 4.0.4 on 2022-04-24 09:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0005_projectattachment_attachement'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ProjectAttachment',
        ),
        migrations.AlterModelOptions(
            name='attachement',
            options={},
        ),
        migrations.RemoveField(
            model_name='attachement',
            name='polymorphic_ctype',
        ),
    ]
