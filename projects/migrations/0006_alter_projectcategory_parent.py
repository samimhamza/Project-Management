# Generated by Django 4.0.4 on 2022-06-21 12:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0005_alter_projectcategory_parent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectcategory',
            name='parent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='projects.projectcategory'),
        ),
    ]
