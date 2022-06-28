from common.actions import (withTrashed, trashList, delete, restore, allItems,
                            filterRecords, expensesOfProject, addAttachment, deleteAttachments, getAttachments)
from expenses.models import Expense, ExpenseItem, Category
from common.permissions_scopes import ExpensePermissions
from common.custom import CustomPageNumberPagination
from projects.models import Project
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import viewsets, status
from expenses.api.serializers import (
    CategorySerializer,
    CategoryTrashedSerializer,
    ExpenseSerializer,
    LessFieldExpenseSerializer,
    ExpenseTrashedSerializer,
    ExpenseItemSerializer,
    ExpenseItemTrashedSerializer,
    CategoryListSerializer
)
from users.models import User


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.filter(
        deleted_at__isnull=True).order_by("-created_at")
    serializer_class = CategorySerializer
    pagination_class = CustomPageNumberPagination
    permission_classes = (ExpensePermissions,)
    serializer_action_classes = {
        "trashed": CategoryTrashedSerializer
    }
    queryset_actions = {
        "destroy": Category.objects.all(),
    }

    def list(self, request):
        queryset = self.get_queryset()
        queryset = filterRecords(queryset, request, table=Expense)
        if request.GET.get("items_per_page") == "-1":
            return allItems(CategoryListSerializer, queryset)

        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    def destroy(self, request, pk=None):
        return delete(self, request, Category)

    @ action(detail=False, methods=["get"])
    def all(self, request):
        return withTrashed(self, Category, order_by="-created_at")

    @ action(detail=False, methods=["get"])
    def trashed(self, request):
        return trashList(self, Category)

    # for multi restore
    @ action(detail=False, methods=["put"])
    def restore(self, request, pk=None):
        return restore(self, request, Category)

    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()

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
    serializer_action_classes = {
        "trashed": ExpenseTrashedSerializer
    }
    queryset_actions = {
        "destroy": Expense.objects.all(),
    }

    def list(self, request):
        queryset = self.get_queryset()
        queryset = filterRecords(queryset, request, table=Expense)
        if request.GET.get("project_id"):
            return expensesOfProject(self, request)

        if request.GET.get("items_per_page") == "-1":
            return allItems(LessFieldExpenseSerializer, queryset)

        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    def retrieve(self, request, pk=None):
        expense = self.get_object()
        serializer = self.get_serializer(expense)
        data = serializer.data
        data = getAttachments(request, data, expense.id,
                              "expense_attachments_v")
        return Response(data)

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
        serializer = self.get_serializer(new_Task)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        expense = self.get_object()
        data = request.data
        if "category" in data:
            category = Category.objects.only('id').get(pk=data['category'])
            expense.category = category
        expense_by = get_object_or_404(User, pk=data['expense_by'])
        expense.expense_by = expense_by
        for key, value in request.data.items():
            if key != "category" and key != "id":
                setattr(expense, key, value)
        expense.updated_by = request.user
        expense.save()
        serializer = self.get_serializer(expense)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def destroy(self, request, pk=None):
        return delete(self, request, Expense)

    @ action(detail=False, methods=["get"])
    def all(self, request):
        return withTrashed(self, Expense, order_by="-created_at")

    @ action(detail=False, methods=["get"])
    def trashed(self, request):
        return trashList(self, Expense)

    # for multi restore
    @ action(detail=False, methods=["put"])
    def restore(self, request, pk=None):
        return restore(self, request, Expense)

    @ action(detail=True, methods=["post"])
    def add_attachments(self, request, pk=None):
        return addAttachment(self, request)

    @ action(detail=True, methods=["delete"])
    def delete_attachments(self, request, pk=None):
        return deleteAttachments(self, request)

    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()

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
    serializer_action_classes = {
        "trashed": ExpenseItemTrashedSerializer
    }
    queryset_actions = {
        "destroy": ExpenseItem.objects.all(),
    }

    def list(self, request):
        queryset = self.get_queryset()
        queryset = filterRecords(queryset, request, table=ExpenseItem)
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

    @ action(detail=False, methods=["get"])
    def all(self, request):
        return withTrashed(self, ExpenseItem, order_by="-created_at")

    @ action(detail=False, methods=["get"])
    def trashed(self, request):
        return trashList(self, ExpenseItem)

    # for multi restore
    @ action(detail=False, methods=["put"])
    def restore(self, request, pk=None):
        return restore(self, request, ExpenseItem)

    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()

    def get_queryset(self):
        try:
            return self.queryset_actions[self.action]
        except (KeyError, AttributeError):
            return super().get_queryset()
