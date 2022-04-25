import uuid
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation
from django.core.validators import RegexValidator


class Attachment(models.Model):
    name = models.CharField(max_length=64)
    path = models.CharField(max_length=255)

    # Below the mandatory fields for generic relation
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    def __str__(self):
        return self.name


class Reason(models.Model):
    description = models.TextField()

    # Below the mandatory fields for generic relation
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()


class Country(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class Location(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    address_line_one = models.TextField()
    address_line_two = models.TextField()
    city = models.CharField(max_length=64)
    state = models.CharField(max_length=64)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)
    latitude = models.CharField(max_length=128, null=True, blank=True)
    longitude = models.CharField(max_length=128, null=True, blank=True)
    created_by = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        related_name="location_created_by",
    )
    updated_by = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        related_name="location_updated_by",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.city + " " + self.state


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
    company_location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True)
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
    attachments = GenericRelation(Attachment)
    reasons = GenericRelation(Reason)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    users = models.ManyToManyField("users.User", related_name="project_user")

    def __str__(self):
        return self.name


class Income(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=128)
    description = models.TextField()
    amount = models.FloatField()

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
        on_delete=models.SET_NULL,
        null=True,
        related_name="income_updated_by",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)


class Payment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    income = models.ForeignKey(Income, on_delete=models.SET_NULL, null=True)
    source = models.CharField(max_length=255)
    amount = models.FloatField()

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


class FocalPoint(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True)
    contact_name = models.CharField(max_length=64)
    contact_last_name = models.CharField(max_length=64)
    email = models.EmailField()
    phone_regex = RegexValidator(
        regex=r"^\+?1?\d{9,15}$",
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.",
    )
    phone = models.CharField(validators=[phone_regex], max_length=17)
    whatsapp = models.CharField(validators=[phone_regex], max_length=17)
    position = models.CharField(max_length=64)
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
