import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    profile = models.ImageField(
        upload_to="user_profiles", blank=True, null=True)
    phone = models.CharField(max_length=32, blank=True, null=True)
    whatsapp = models.CharField(max_length=64, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="user_created_by",
    )
    updated_by = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="user_updated_by",
    )
    deleted_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.first_name + " " + self.last_name


class Team(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=64)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="team_created_by",
    )
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="team_updated_by",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    users = models.ManyToManyField(
        User, through="TeamUser", related_name="%(class)ss")
    deleted_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.name


class TeamUser(models.Model):
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    position = models.CharField(max_length=64, blank=True, null=True)
    is_leader = models.BooleanField(default=False)

    def __str__(self):
        if self.position:
            return self.position
        else:
            return "No Position"


class Reminder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    note = models.TextField()
    remind_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name + " " + self.remind_at


class Holiday(models.Model):
    title = models.CharField(max_length=128)
    start_date = models.DateField()
    end_date = models.DateField()


class Notification(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    icon = models.CharField(max_length=255)

    class Types(models.TextChoices):
        notify = "notify"
        error = "error"
        success = "success"
        warning = "warning"

    type = models.CharField(
        max_length=24, choices=Types.choices, default="notify")
