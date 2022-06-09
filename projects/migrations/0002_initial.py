# Generated by Django 4.0.4 on 2022-06-09 04:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('projects', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0001_initial'),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='project_created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='project',
            name='teams',
            field=models.ManyToManyField(related_name='%(class)ss', to='users.team'),
        ),
        migrations.AddField(
            model_name='project',
            name='updated_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='project_updated_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='project',
            name='users',
            field=models.ManyToManyField(related_name='project_users', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='payment',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='payment_created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='payment',
            name='income',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='payments', to='projects.income'),
        ),
        migrations.AddField(
            model_name='payment',
            name='updated_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='payment_updated_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='location',
            name='project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='company_location', to='projects.project'),
        ),
        migrations.AddField(
            model_name='location',
            name='state',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='projects.state'),
        ),
        migrations.AddField(
            model_name='income',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='income_created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='income',
            name='project',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='projects.project'),
        ),
        migrations.AddField(
            model_name='income',
            name='updated_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='income_updated_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='focalpoint',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='focalPoint_created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='focalpoint',
            name='project',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='projects.project'),
        ),
        migrations.AddField(
            model_name='focalpoint',
            name='updated_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='focalPoint_updated_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='attachment',
            name='content_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype'),
        ),
        migrations.AddIndex(
            model_name='reason',
            index=models.Index(fields=['content_type', 'object_id'], name='projects_re_content_bf70f3_idx'),
        ),
        migrations.AddIndex(
            model_name='attachment',
            index=models.Index(fields=['content_type', 'object_id'], name='projects_at_content_b96819_idx'),
        ),
    ]
