from unicodedata import name
import uuid
from django.db import models


class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=128)


class Expense(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=128)
    project = models.ForeignKey(
        "projects.Project", on_delete=models.SET_NULL, null=True
    )
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    body = models.TextField()
    coast = models.DecimalField(max_digits=19, decimal_places=2)

    class Types(models.TextChoices):
        estimate = "estimate"
        actual = "actual"

    type = models.CharField(max_length=24, choices=Types.choices, default="actual")
    expense_by = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        related_name="expense_by",
    )
    created_by = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        related_name="expense_created_by",
    )
    updated_by = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        related_name="expense_updated_by",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)


class ExpenseItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    expense = models.ForeignKey(Expense, on_delete=models.SET_NULL, null=True)
    item = models.CharField(max_length=255)
    quantity = models.IntegerField()
    cpp = models.DecimalField(max_digits=19, decimal_places=2)
    unit = models.CharField(max_length=64)
