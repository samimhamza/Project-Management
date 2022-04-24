from django.db import models

# Create your models here.
class Project(models.Model):
    id                  = models.UUIDField(max_length=30)
    name                = models.CharField(max_length=30)
    description         = models.TextField()
    p_start_date        = models.DateTimeField()
    p_end_date          = models.DateTimeField()
    a_start_date        = models.DateTimeField()
    a_end_date          = models.DateTimeField()
    banner              = models.CharField(max_length=120)
    status              = models.IntegerField()
    progress            = models.IntegerField()
    priority            = models.IntegerField()
    project_details     = models.JSONField()
    company_name        = models.CharField(max_length=100)
    company_location    = models.CharField(max_length=100)
    created_at          = models.DateTimeField()
    updated_at          = models.DateTimeField()
