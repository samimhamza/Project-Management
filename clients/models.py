from django.contrib.contenttypes.fields import GenericRelation
from projects.models import Country, Attachment
from django.db import models
import uuid


class Service(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    parent = models.ForeignKey(
        "self", on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=128)
    description = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        related_name="service_created_by"
    )
    updated_by = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        related_name="service_updated_by"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    deleted_by = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="service_deleted_by",
    )

    def __str__(self):
        return self.name


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=128)
    developed_by = models.CharField(max_length=128, blank=True, null=True)
    details = models.TextField(blank=True, null=True)
    photo = models.ImageField(
        upload_to="products", blank=True, null=True
    )
    created_by = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        related_name="product_created_by"
    )
    updated_by = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        related_name="product_updated_by"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    deleted_by = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="product_deleted_by",
    )

    def __str__(self):
        return self.name


class Feature(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=128)
    description = models.TextField(null=True, blank=True)

    class Types(models.TextChoices):
        main = "main"
        additional = "additional"

    type = models.CharField(
        max_length=24, choices=Types.choices, default="main"
    )
    product = models.ForeignKey(
        Product, null=True, on_delete=models.CASCADE, related_name="product_features")

    def __str__(self):
        return self.name


class Client(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=32, blank=True, null=True)
    whatsapp = models.CharField(max_length=64, blank=True, null=True)
    profile = models.ImageField(
        upload_to="client_profiles", blank=True, null=True)
    country = models.ForeignKey(
        Country,
        on_delete=models.SET_NULL,
        null=True,
        related_name="client_country",
    )
    company_name = models.CharField(max_length=128, blank=True, null=True)
    industry = models.CharField(max_length=128, blank=True, null=True)
    services = models.ManyToManyField(
        Service, through="ClientService", related_name="%(class)ss"
    )
    features = models.ManyToManyField(
        Feature, through="ClientFeature", related_name="%(class)ss"
    )

    class HearAboutUs(models.TextChoices):
        search_engine = "search_engine"
        google_ads = "google_ads"
        facebook_ads = "facebook_ads"
        instagram_ads = "instagram_ads"
        youtube_ads = "youtube_ads"
        linkedin_ads = "linkedin_ads"
        snapchat_ads = "snapchat_ads"
        twitter_ads = "twitter_ads"
        tiktok_ads = "tiktok_ads"
        other_social_media_ads = "other_social_media_ads"
        email = "email"
        radio = "radio"
        tv = "tv"
        newspaper = "newspaper"
        word_of_mouth = "word_of_mouth"
        other = "other"

    hear_about_us = models.CharField(
        max_length=64, choices=HearAboutUs.choices, blank=True, null=True
    )

    class LeadType(models.TextChoices):
        manual = "manual"
        website = "website"
        facebook = "facebook"
        instagram = "instagram"
        twitter = "twitter"
        linkedin = "linkedin"
        youtube = "youtube"
        tiktok = "tiktok"
        whatsapp = "whatsapp"
        other = "other"

    lead_type = models.CharField(
        max_length=64, choices=LeadType.choices, blank=True, null=True
    )

    class PreferComWay(models.TextChoices):
        email = "email"
        phone = "phone"
        whatsapp = "whatsapp"

    prefer_com_way = models.CharField(
        max_length=32, choices=PreferComWay.choices, blank=True, null=True
    )

    is_requirement_ready = models.BooleanField(default=False)
    need_for_demo = models.BooleanField(default=False)

    class statusChoices(models.TextChoices):
        pending = "pending"
        need_to_communicate = "need_to_communicate"
        not_interested = "not_interested"
        not_answered = "not_answered"
        not_interest_now = "not_interested_now"
        incorrect_contact = "incorrect_contact"
        check_and_come_back = "check_and_come_back"
        understood_wrong = "understood_wrong"
        confirm = "confirm"

    status = models.CharField(
        max_length=32, choices=statusChoices.choices, default="pending"
    )

    date = models.DateField(blank=True, null=True)
    created_by = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        related_name="client_created_by"
    )
    updated_by = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        related_name="client_updated_by"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    deleted_by = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="client_deleted_by",
    )

    def __str__(self):
        return self.first_name


class ClientService(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    service = models.ForeignKey(
        Service, null=True, on_delete=models.SET_NULL, related_name='clientService_service')
    client = models.ForeignKey(
        Client, null=True, on_delete=models.SET_NULL, related_name='clientService_client')
    details = models.TextField(blank=True, null=True)
    attachments = GenericRelation(
        Attachment,
        content_type_field="content_type",
        object_id_field="object_id",
        related_query_name='comments'
    )

    def __str__(self):
        if self.client:
            return self.client.first_name
        else:
            return self.details


class PricePlan(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    plan_name = models.CharField(max_length=128)
    plan_price = models.FloatField(max_length=120, null=True, blank=True)
    duration = models.IntegerField()
    feature = models.ForeignKey(
        Feature, null=True, on_delete=models.CASCADE, related_name="price_plans")

    def __str__(self):
        return self.plan_name


class ClientFeature(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    feature = models.ForeignKey(Feature, null=True, on_delete=models.SET_NULL)
    plan = models.CharField(max_length=32, blank=True, null=True)
    on_request_price = models.FloatField(max_length=255, null=True, blank=True)
    on_request_date = models.DateTimeField(blank=True, null=True)
    purchased_price = models.FloatField(max_length=255, null=True, blank=True)
    purchased_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    client = models.ForeignKey(Client, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        if self.client:
            return self.client.first_name + " " \
                + (self.feature.name if self.feature else "") + \
                " " + self.plan if self.plan else ""
        else:
            return "No Client"


class Requirement(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    client = models.OneToOneField(Client, on_delete=models.CASCADE)

    class statusChoices(models.TextChoices):
        pending = "pending"
        review = "review"
        confirm = "confirm"
        reject = "reject"
        miss_info = "miss_info"

    status = models.CharField(
        max_length=32, choices=statusChoices.choices, default="pending")
    goals_and_expectation = models.JSONField(blank=True, null=True)
    budget = models.FloatField(max_length=255, blank=True, null=True)
    currency = models.CharField(max_length=32, blank=True, null=True)
    project_timeline_start = models.DateField(blank=True, null=True)
    project_timeline_end = models.DateField(blank=True, null=True)
    frequently_of_receive_progress_report = models.TextField(
        blank=True, null=True)
    what_are_we_delivering = models.TextField(blank=True, null=True)
    what_are_we_not_delivering = models.TextField(blank=True, null=True)
    target_audience = models.JSONField(blank=True, null=True)
    target_gender = models.JSONField(blank=True, null=True)
    target_age = models.JSONField(blank=True, null=True)
    technologies = models.JSONField(blank=True, null=True)
    functionalities = models.JSONField(blank=True, null=True)
    tools = models.JSONField(blank=True, null=True)
    data_storing_requirements = models.JSONField(blank=True, null=True)
    restrictions = models.JSONField(blank=True, null=True)
    confidentiality = models.TextField(blank=True, null=True)
    how_many_people_use_this = models.IntegerField(blank=True, null=True)
    created_by = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        related_name="requirement_created_by"
    )
    updated_by = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        related_name="requirement_updated_by"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    deleted_by = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="requirement_deleted_by",
    )

    def __str__(self):
        if self.goals_and_expectation:
            return self.goals_and_expectation
        else:
            return "No Goal"
