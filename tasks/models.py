import uuid
from django.db import models
from projects.models import Project, Attachement
from django.contrib.contenttypes.fields import GenericRelation
from softdelete.models import SoftDeleteObject

# Start of Task Table
class Task(SoftDeleteObject, models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    projects = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=64)
    description = models.TextField(blank=True, null=True)
    p_start_date = models.DateTimeField(blank=True, null=True)
    p_end_date = models.DateTimeField(blank=True, null=True)
    a_start_date = models.DateTimeField(blank=True, null=True)
    a_end_date = models.DateTimeField(blank=True, null=True)

    class Priority(models.TextChoices):
        critical = "critical"
        very_important = "very_important"
        important = "important"
        normal = "normal"
        less_important = "less_important"

    priority = models.CharField(
        max_length=24, choices=Priority.choices, default="normal"
    )

    class StatusChoices(models.TextChoices):
        pending = "pending"
        in_progress = "in_progress"
        completed = "completed"
        very_important = "issue_faced"
        failed = "failed"
        cancelled = "cancelled"

    status = models.CharField(
        max_length=24, choices=StatusChoices.choices, default="pending"
    )

    class Types(models.TextChoices):
        dependent = "dependent"
        independent = "independent"

    type = models.CharField(max_length=24, choices=Types.choices, default="independent")
    created_by = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        related_name="task_created_by",
    )
    updated_by = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        related_name="task_updated_by",
    )
    attachements = GenericRelation(Attachement)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


# End of Task Table

# start of UserTask Table
class UserTask(SoftDeleteObject, models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = models.TextField(blank=True, null=True)
    user = models.ForeignKey("users.User", on_delete=models.SET_NULL, null=True)
    task = models.ForeignKey(Task, on_delete=models.SET_NULL, null=True)
    progress = models.FloatField()

    class UserTaskTypes(models.TextChoices):
        assign = "assign"
        revoke = "revoke"

    type = models.CharField(
        max_length=24, choices=UserTaskTypes.choices, default="revoke"
    )
    created_by = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        related_name="user_task_created_by",
    )
    updated_by = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        related_name="user_task_updated_by",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.description


# End of UserTask Table

# Start of Comments Table
class Comments(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    body = models.TextField()
    task = models.ForeignKey(Task, on_delete=models.SET_NULL, null=True)
    commented_by = models.ForeignKey("users.User", on_delete=models.CASCADE)
    attachements = GenericRelation(Attachement)

    def __str__(self):
        return self.body


# end of Comments Table

# class Attachement(models.Model):
#     attachmentable_id = models.CharField(max_length=64)
#     attachmentable_type = models.CharField(max_length=32)
#     name = models.CharField(max_length=64)
#     path = models.CharField(max_length=255)
