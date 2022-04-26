from rest_framework import serializers
from expenses.models import Category, Expense, ExpenseItem


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = "__all__"


class ExpenseItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseItem
        fields = "__all__"
