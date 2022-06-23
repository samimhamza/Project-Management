from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.db import models
import uuid


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
    deleted_by = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="user_deleted_by",
    )

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
    deleted_by = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="team_deleted_by",
    )

    def __str__(self):
        return self.name


class TeamUser(models.Model):
    team = models.ForeignKey(
        Team, on_delete=models.SET_NULL, null=True, related_name='team')
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='user')
    position = models.CharField(max_length=64, blank=True, null=True)
    is_leader = models.BooleanField(default=False)

    def __str__(self):
        if self.position:
            return self.position
        else:
            return "No Position"

    class Meta:
        unique_together = ('team', 'user',)


class Reminder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    note = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    remind_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.user.first_name + " " + self.note


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
    users = models.ManyToManyField(
        User, through="UserNotification", related_name="user_notifications", through_fields=('notification', 'receiver'))


class UserNotification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    seen = models.BooleanField(default=False)
    sender = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="sender",
    )
    receiver = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="receiver",
    )
    notification = models.ForeignKey(
        Notification, on_delete=models.CASCADE, related_name="notification")
    description = models.TextField(blank=True, null=True)
    model_name = models.CharField(max_length=128, blank=True, null=True)
    instance_id = models.CharField(max_length=128, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Role(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=64, unique=True)
    users = models.ManyToManyField(
        User, related_name="roles_users")
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="role_created_by",
    )
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="role_updated_by",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    deleted_by = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="role_deleted_by",
    )

    def __str__(self):
        return self.name


class SubAction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=32, unique=True)
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name


class Action(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=64, unique=True)
    codename = models.CharField(max_length=64, unique=True)
    model = models.CharField(max_length=64, unique=True)
    order = models.IntegerField(null=True)

    def __str__(self):
        return self.name


class Permission(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    action = models.ForeignKey(
        Action, on_delete=models.CASCADE, related_name="permission_action")
    sub_action = models.ForeignKey(
        SubAction, on_delete=models.CASCADE, related_name="permission_sub_action")
    roles = models.ManyToManyField(
        Role, related_name="permissions_roles")
    users = models.ManyToManyField(
        User, related_name="permissions_users")
    proles = models.ManyToManyField(
        'projects.ProjectRole', related_name="projects_permissions")


class UserPermissionList(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="userpermissions")
    permissions_list = models.JSONField(blank=True, null=True)


class PasswordReset(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="resets")
    created_at = models.DateTimeField(auto_now_add=True)
