import uuid
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation
from django.core.validators import RegexValidator


class Attachment(models.Model):
    name = models.CharField(max_length=64)
    attachment = models.FileField(upload_to="attachments")
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


class Reason(models.Model):
    description = models.TextField()

    # Below the mandatory fields for generic relation
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.UUIDField()
    content_object = GenericForeignKey("content_type", "object_id")

    def __str__(self):
        return self.content_type.app_name

    class Meta:
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]


class Country(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=64, blank=True, null=True, unique=True)

    def __str__(self):
        if self.name:
            return self.name
        else:
            return "No Name"


class Project(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=30, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    p_start_date = models.DateField(null=True, blank=True)
    p_end_date = models.DateField(null=True, blank=True)
    a_start_date = models.DateField(null=True, blank=True)
    a_end_date = models.DateField(null=True, blank=True)
    banner = models.CharField(max_length=120, null=True, blank=True)

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
    project_details = models.JSONField(null=True, blank=True)
    company_name = models.CharField(max_length=100, null=True, blank=True)
    company_email = models.EmailField(null=True, blank=True)
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
    attachments = GenericRelation(
        Attachment,
        content_type_field="content_type",
        object_id_field="object_id",
        related_query_name='projects'
    )
    reasons = GenericRelation(
        Reason, content_type_field="content_type", object_id_field="object_id",
        related_query_name='projects'
    )
    comments = GenericRelation(
        'tasks.Comment',
        content_type_field="content_type",
        object_id_field="object_id",
        related_query_name='projects'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    users = models.ManyToManyField("users.User", related_name="project_users")
    teams = models.ManyToManyField(
        "users.Team", related_name="%(class)ss")

    def __str__(self):
        if self.name:
            return self.name
        else:
            return "No Name"


class Location(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    address_line_one = models.TextField(blank=True, null=True)
    address_line_two = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=64, blank=True, null=True)
    state = models.CharField(max_length=64, blank=True, null=True)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)
    latitude = models.CharField(max_length=128, null=True, blank=True)
    longitude = models.CharField(max_length=128, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    project = models.ForeignKey(
        Project,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="company_location",
    )

    def __str__(self):
        if self.city and self.state:
            return self.city + " " + self.state
        else:
            return "No City Added"


class Income(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=128)
    description = models.TextField(blank=True, null=True)
    amount = models.DecimalField(max_digits=19, decimal_places=2,blank=True, null=True)

    class Types(models.TextChoices):
        initial_cost = "initial_cost"
        maintenance = "maintenance"
        upgrades = "upgrades"

    type = models.CharField(
        max_length=24, choices=Types.choices, default="initial_cost"
    )
    created_by = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        related_name="income_created_by",
    )
    updated_by = models.ForeignKey(
        "users.User",
        null=True,
        related_name="income_updated_by",
        on_delete=models.SET_NULL,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.title


class Payment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    income = models.ForeignKey(Income, on_delete=models.SET_NULL, null=True, related_name='payments')
    source = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=19, decimal_places=2)

    class PaymentMethods(models.TextChoices):
        cash = "cash"
        credit_card = "credit_card"
        bank_transaction = "bank_transaction"

    payment_method = models.CharField(
        max_length=24, choices=PaymentMethods.choices, default="cash"
    )
    created_by = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        related_name="payment_created_by",
    )
    updated_by = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        related_name="payment_updated_by",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.source


class FocalPoint(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True)
    contact_name = models.CharField(max_length=64)
    contact_last_name = models.CharField(max_length=64, blank=True, null=True)
    email = models.EmailField()
    phone_regex = RegexValidator(
        regex=r"^\+?1?\d{9,15}$",
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.",
    )
    phone = models.CharField(
        validators=[phone_regex], max_length=17, blank=True, null=True)
    whatsapp = models.CharField(
        validators=[phone_regex], max_length=17, blank=True, null=True)
    position = models.CharField(max_length=64, blank=True, null=True)
    created_by = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        related_name="focalPoint_created_by",
    )
    updated_by = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        related_name="focalPoint_updated_by",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class PreferMethods(models.TextChoices):
        email = "email"
        whatsapp = "whatsapp"
        phone = "phone"

    prefer_communication_way = models.CharField(
        max_length=16, choices=PreferMethods.choices, default="email"
    )

    def __str__(self):
        return self.contact_name + " " + self.contact_last_name
