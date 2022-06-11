from common.actions import withTrashed, trashList, delete, restore, allItems, filterRecords, expensesOfProject
from common.permissions_scopes import ExpensePermissions
from expenses.models import Expense, ExpenseItem, Category
from common.custom import CustomPageNumberPagination
from expenses.api.serializers import (
    ExpenseSerializer,
    ExpenseItemSerializer,
    CategorySerializer,
    LessFieldExpenseSerializer
)
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from projects.models import Project
from users.models import User


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.filter(
        deleted_at__isnull=True).order_by("-created_at")
    serializer_class = CategorySerializer
    pagination_class = CustomPageNumberPagination
    permission_classes = (ExpensePermissions,)
    queryset_actions = {
        "destroy": Category.objects.all(),
    }

    def destroy(self, request, pk=None):
        return delete(self, request, Category)

    @action(detail=False, methods=["get"])
    def all(self, request):
        return withTrashed(self, Category, order_by="-created_at")

    @action(detail=False, methods=["get"])
    def trashed(self, request):
        return trashList(self, Category)

    # for multi restore
    @action(detail=False, methods=["get"])
    def restore(self, request, pk=None):
        return restore(self, request, Category)

    def get_queryset(self):
        try:
            return self.queryset_actions[self.action]
        except (KeyError, AttributeError):
            return super().get_queryset()


class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.filter(
        deleted_at__isnull=True).order_by("-created_at")
    serializer_class = ExpenseSerializer
    pagination_class = CustomPageNumberPagination
    permission_classes = (ExpensePermissions,)
    queryset_actions = {
        "destroy": Expense.objects.all(),
    }

    def list(self, request):
        queryset = self.get_queryset()
        queryset = filterRecords(queryset, request)
        if request.GET.get("project_id"):
            return expensesOfProject(self, request)

        if request.GET.get("items_per_page") == "-1":
            return allItems(LessFieldExpenseSerializer, queryset)

        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    def create(self, request):
        data = request.data
        creator = request.user
        if data['category']:
            category = Category.objects.only('id').get(pk=data['category'])
        else:
            category = None
        if data['project']:
            project = Project.objects.only('id').get(pk=data['project'])
        else:
            project = None
        expense_by = get_object_or_404(User, pk=data['expense_by'])
        new_Task = Expense.objects.create(
            category=category,
            title=data["title"],
            date=data["date"],
            project=project,
            expense_by=expense_by,
            type=data["type"],
            created_by=creator,
            updated_by=creator,
        )
        new_Task.save()
        serializer = ExpenseSerializer(new_Task)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        expense = self.get_object()
        data = request.data
        if request.data.get("title"):
            expense.title = request.data.get("title")
        if request.data.get("body"):
            expense.body = request.data.get("body")
        if request.data.get("date"):
            expense.date = request.data.get("date")
        if request.data.get("category"):
            category = Category.objects.only('id').get(pk=data['category'])
            expense.category = category
        expense.updated_by = request.user
        expense.save()
        serializer = ExpenseSerializer(expense)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def destroy(self, request, pk=None):
        return delete(self, request, Expense)

    @action(detail=False, methods=["get"])
    def all(self, request):
        return withTrashed(self, Expense, order_by="-created_at")

    @action(detail=False, methods=["get"])
    def trashed(self, request):
        return trashList(self, Expense)

    # for multi restore
    @action(detail=False, methods=["get"])
    def restore(self, request, pk=None):
        return restore(self, request, Expense)

    def get_queryset(self):
        try:
            return self.queryset_actions[self.action]
        except (KeyError, AttributeError):
            return super().get_queryset()


class ExpenseItemViewSet(viewsets.ModelViewSet):
    queryset = ExpenseItem.objects.filter(
        deleted_at__isnull=True).order_by("-created_at")
    serializer_class = ExpenseItemSerializer
    pagination_class = CustomPageNumberPagination
    permission_classes = (ExpensePermissions,)
    queryset_actions = {
        "destroy": ExpenseItem.objects.all(),
    }

    def list(self, request):
        queryset = self.get_queryset()
        queryset = filterRecords(queryset, request)
        if request.GET.get("items_per_page") == "-1":
            return allItems(ExpenseItemSerializer, queryset)

        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    def create(self, request):
        data = request.data
        if data['expense']:
            expense = Expense.objects.only('id').get(pk=data['expense'])
        else:
            expense = None
        new_Task = ExpenseItem.objects.create(
            expense=expense,
            name=data["name"],
            cost=data["cost"],
            unit=data["unit"],
            quantity=data['quantity'],
        )
        new_Task.save()
        serializer = ExpenseItemSerializer(new_Task)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk=None):
        return delete(self, request, ExpenseItem)

    @action(detail=False, methods=["get"])
    def all(self, request):
        return withTrashed(self, ExpenseItem, order_by="-created_at")

    @action(detail=False, methods=["get"])
    def trashed(self, request):
        return trashList(self, ExpenseItem)

    # for multi restore
    @action(detail=False, methods=["get"])
    def restore(self, request, pk=None):
        return restore(self, request, ExpenseItem)

    def get_queryset(self):
        try:
            return self.queryset_actions[self.action]
        except (KeyError, AttributeError):
            return super().get_queryset()
