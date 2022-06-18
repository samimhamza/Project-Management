from expenses.models import Category, Expense, ExpenseItem
from users.api.serializers import UserWithProfileSerializer
from rest_framework import serializers
from projects.api.project.serializers import ProjectListSerializer


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ExpenseItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseItem
        fields = "__all__"


class ExpenseSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()
    category = CategorySerializer()
    expense_by = UserWithProfileSerializer()

    def get_items(self, expense):
        qs = ExpenseItem.objects.filter(
            deleted_at__isnull=True, expense=expense)
        serializer = ExpenseItemSerializer(instance=qs, many=True)
        return serializer.data

    class Meta:
        model = Expense
        fields = "__all__"


class ExpenseListSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()
    category = CategorySerializer()
    expense_by = UserWithProfileSerializer()
    project = ProjectListSerializer()

    def get_items(self, expense):
        qs = ExpenseItem.objects.filter(
            deleted_at__isnull=True, expense=expense)
        serializer = ExpenseItemSerializer(instance=qs, many=True)
        return serializer.data

    class Meta:
        model = Expense
        fields = "__all__"


class LessFieldExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ["id", "title", "data"]
