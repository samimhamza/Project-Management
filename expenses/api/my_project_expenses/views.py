from common.actions import (allItems, filterRecords, expensesOfProject,
                            addAttachment, deleteAttachments, getAttachments, delete, checkAndReturn)
from expenses.models import Expense, ExpenseItem, Category
from rest_framework.permissions import IsAuthenticated
from common.custom import CustomPageNumberPagination
from expenses.actions import totalExpenseAndIncome, categoryList
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status, viewsets
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
from projects.models import Project
from projects.models import Income
from users.models import User


class MyCategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.filter(
        deleted_at__isnull=True).order_by("-created_at")
    pagination_class = CustomPageNumberPagination
    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticated,)
    serializer_action_classes = {
        "trashed": CategoryTrashedSerializer
    }
    queryset_actions = {
        "destroy": Category.objects.all(),
    }

    def list(self, request):
        return checkAndReturn(request.user, income.project, "project_expenses_v",
                              categoryList(self, request, CategoryListSerializer))

    def create(self, request):
        data = request.data
        creator = request.user
        category = Category.objects.create(
            name=data["name"],
            created_by=creator,
            updated_by=creator,
        )
        category.save()
        serializer = self.get_serializer(category)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        category = self.get_object()
        for key, value in request.data.items():
            setattr(category, key, value)
        category.updated_by = request.user
        category.save()
        serializer = self.get_serializer(category)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def destroy(self, request, pk=None):
        return delete(self, request, Category)

    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except(KeyError, AttributeError):
            return super().get_serializer_class()

    def get_queryset(self):
        try:
            return self.queryset_actions[self.action]
        except (KeyError, AttributeError):
            return super().get_queryset()


class MyExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.filter(
        deleted_at__isnull=True).order_by("-created_at")
    pagination_class = CustomPageNumberPagination
    serializer_class = ExpenseSerializer
    permission_classes = (IsAuthenticated,)
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
            return expensesOfProject(self, request, queryset)

        if request.GET.get("items_per_page") == "-1":
            return allItems(LessFieldExpenseSerializer, queryset)

        serializer = self.get_serializer(
            queryset, many=True, context={"request": request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        expense = self.get_object()
        serializer = self.get_serializer(expense, context={"request": request})
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
        try:
            expense_by = User.objects.only('id').get(pk=data['expense_by'])
        except User.DoesNotExist:
            return Response({"error": "User does not exist!"}, status=status.HTTP_404_NOT_FOUND)

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
        serializer = self.get_serializer(
            new_Task, context={"request": request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        expense = self.get_object()
        data = request.data
        if "category" in data:
            try:
                category = Category.objects.only('id').get(pk=data['category'])
                expense.category = category
            except Category.DoesNotExist:
                return Response({"error": "Category does not exist!"}, status=status.HTTP_404_NOT_FOUND)
        if "expense_by" in data:
            try:
                expense_by = User.objects.only('id').get(pk=data['expense_by'])
                expense.expense_by = expense_by
            except User.DoesNotExist:
                return Response({"error": "User does not exist!"}, status=status.HTTP_404_NOT_FOUND)
        for key, value in request.data.items():
            if key != "category" and key != "id" and key != "expense_by":
                setattr(expense, key, value)
        expense.updated_by = request.user
        expense.save()
        serializer = self.get_serializer(expense, context={"request": request})
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    @ action(detail=True, methods=["post"])
    def add_attachments(self, request, pk=None):
        try:
            expense = self.get_object()
            return addAttachment(request, expense)
        except:
            return Response(
                {"message": "something went wrong"}, status=status.HTTP_400_BAD_REQUEST
            )

    @ action(detail=True, methods=["delete"])
    def delete_attachments(self, request, pk=None):
        return deleteAttachments(self, request)

    @ action(detail=False, methods=["get"])
    def income_expense_reports(self, request, pk=None):
        if request.query_params.get('year'):
            if request.query_params.get('project_id'):
                expenses = ExpenseItem.objects.filter(
                    deleted_at__isnull=True, expense__type='actual', expense__project=request.GET['project_id'])
                incomes = Income.objects.filter(
                    deleted_at__isnull=True, project=request.GET['project_id'])
            else:
                expenses = ExpenseItem.objects.filter(
                    deleted_at__isnull=True, expense__type='actual')
                incomes = Income.objects.filter(deleted_at__isnull=True)

            results = totalExpenseAndIncome(
                expenses, incomes, request.GET['year'])
            return Response(results)
        else:
            return Response({"detail": "Year is not selected"}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        return delete(self, request, Expense)

    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except(KeyError, AttributeError):
            return super().get_serializer_class()

    def get_queryset(self):
        try:
            return self.queryset_actions[self.action]
        except (KeyError, AttributeError):
            return super().get_queryset()


class MyExpenseItemViewSet(viewsets.ModelViewSet):
    model = ExpenseItem
    queryset = ExpenseItem.objects.filter(
        deleted_at__isnull=True).order_by("-created_at")
    pagination_class = CustomPageNumberPagination
    serializer_class = ExpenseItemSerializer
    permission_classes = (IsAuthenticated,)
    serializer_action_classes = {
        "trashed": ExpenseItemTrashedSerializer
    }
    queryset_actions = {
        "destroy": ExpenseItem.objects.all(),
    }

    def list(self, request):
        return Response([])

    def retrieve(self, request):
        return Response([])

    def create(self, request):
        data = request.data
        creator = request.user
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
            created_by=creator,
            updated_by=creator,
        )
        new_Task.save()
        serializer = self.get_serializer(
            new_Task, context={"request": request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        item = self.get_object()
        for key, value in request.data.items():
            setattr(item, key, value)
        item.updated_by = request.user
        item.save()
        serializer = self.get_serializer(item, context={"request": request})
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def destroy(self, request, pk=None):
        return delete(self, request, ExpenseItem)

    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except(KeyError, AttributeError):
            return super().get_serializer_class()

    def get_queryset(self):
        try:
            return self.queryset_actions[self.action]
        except (KeyError, AttributeError):
            return super().get_queryset()
