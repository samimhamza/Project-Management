from django.db import models
import uuid


class Project(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=30)
    description = models.TextField()
    p_start_date = models.DateTimeField()
    p_end_date = models.DateTimeField()
    a_start_date = models.DateTimeField()
    a_end_date = models.DateTimeField()
    banner = models.CharField(max_length=120)
    status = models.IntegerField()
    progress = models.IntegerField()
    priority = models.IntegerField()
    project_details = models.JSONField()
    company_name = models.CharField(max_length=100)
    company_location = models.CharField(max_length=100)
    created_by = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        related_name="project_created_by",
    )
    updated_by = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        related_name="project_updated_by",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    user = models.ManyToManyField("users.User", related_name="project_user")

    def __str__(self):
        return self.name
