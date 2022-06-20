import uuid
from django.db import models
from projects.models import Project, Attachment, Reason
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class Comment(models.Model):
    body = models.TextField()
    commented_by = models.ForeignKey("users.User", on_delete=models.CASCADE)
    attachments = GenericRelation(
        Attachment,
        content_type_field="content_type",
        object_id_field="object_id",
        related_query_name='comments'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Below the mandatory fields for generic relation
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.UUIDField()
    content_object = GenericForeignKey("content_type", "object_id")

    def __str__(self):
        return self.content_type.model

    class Meta:
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]


class Task(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    parent = models.ForeignKey(
        "self", on_delete=models.SET_NULL, null=True)
    project = models.ForeignKey(
        Project, on_delete=models.SET_NULL, null=True, related_name="tasks"
    )
    name = models.CharField(max_length=64)
    description = models.TextField(blank=True, null=True)
    p_start_date = models.DateField(blank=True, null=True)
    p_end_date = models.DateField(blank=True, null=True)
    a_start_date = models.DateField(blank=True, null=True)
    a_end_date = models.DateField(blank=True, null=True)
    pin = models.BooleanField(default=False)
    progress = models.IntegerField(default=0)

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
        issue_faced = "issue_faced"
        failed = "failed"
        cancelled = "cancelled"

    status = models.CharField(
        max_length=24, choices=StatusChoices.choices, default="pending"
    )

    class Types(models.TextChoices):
        dependent = "dependent"
        independent = "independent"

    type = models.CharField(
        max_length=24, choices=Types.choices, default="independent")
    dependencies = models.JSONField(blank=True, null=True)
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
    attachments = GenericRelation(
        Attachment,
        content_type_field="content_type",
        object_id_field="object_id",
    )
    reasons = GenericRelation(
        Reason,
        content_type_field="content_type",
        object_id_field="object_id",
    )
    comments = GenericRelation(
        Comment,
        content_type_field="content_type",
        object_id_field="object_id",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    task_users = models.ManyToManyField(
        "users.User",
        through="UserTask",
        through_fields=("task", "user"),
        related_name="users"
    )

    def __str__(self):
        return self.name


# End of Task Table

# start of UserTask Table
class UserTask(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = models.TextField(blank=True, null=True)
    user = models.ForeignKey(
        "users.User", on_delete=models.SET_NULL, null=True, related_name="user_tasks"
    )
    task = models.ForeignKey(
        Task, on_delete=models.SET_NULL, null=True, related_name="users"
    )
    progress = models.IntegerField(default=0)

    class UserTaskTypes(models.TextChoices):
        assign = "assign"
        revoke = "revoke"

    type = models.CharField(
        max_length=24, choices=UserTaskTypes.choices, default="assign"
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
    reasons = GenericRelation(Reason)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.description

    class Meta:
        unique_together = ('task', 'user',)


# End of UserTask Table
