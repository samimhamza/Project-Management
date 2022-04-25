from unicodedata import name
import uuid
from django.db import models
from softdelete.models import SoftDeleteObject


class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=128)


class Expense(SoftDeleteObject, models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=128)
    project = models.ForeignKey(
        "projects.Project", on_delete=models.SET_NULL, null=True
    )
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    body = models.TextField()
    coast = models.FloatField()

    class Types(models.TextChoices):
        estimate = "estimate"
        actual = "actual"

    type = models.CharField(max_length=24, choices=Types.choices, default="actual")
