from expenses.actions import (expenseUpdate, expernseCreate, totalExpenseAndIncome,
                              categoryList, categoryCreate, categoryActions, categoryUpdate, expenseRetrieve)
from common.actions import (filterRecords, expensesOfProject, addAttachment,
                            deleteAttachments, delete, checkProjectScope, unAuthorized, checkAndReturn)
from expenses.models import Expense, ExpenseItem, Category
from rest_framework.permissions import IsAuthenticated
from common.custom import CustomPageNumberPagination
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status, viewsets
from expenses.api.serializers import (
    CategorySerializer,
    CategoryTrashedSerializer,
    ExpenseSerializer,
    ExpenseTrashedSerializer,
    ExpenseItemSerializer,
    ExpenseItemTrashedSerializer,
    CategoryListSerializer
)
from projects.models import Project
from projects.models import Income


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
        return categoryActions(request, "project_expenses_v",
                               categoryList(self, request, CategoryListSerializer))

    def create(self, request):
        return categoryActions(request, "project_expenses_c",
                               categoryCreate(self, request))

    def update(self, request, pk=None):
        return categoryActions(request, "project_expenses_U",
                               categoryUpdate(self, request))

    def destroy(self, request, pk=None):
        return categoryActions(request, "project_expenses_U",
                               delete(self, request, Category))

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
        if request.GET.get("project_id"):
            try:
                project = Project.objects.get(pk=request.GET.get("project_id"))
            except Project.DoesNotExist:
                return unAuthorized()
            if checkProjectScope(request.user, project, "project_expenses_v"):
                queryset = self.get_queryset()
                queryset = filterRecords(queryset, request, table=Income)
                return expensesOfProject(self, request, queryset)
            else:
                return unAuthorized()
        else:
            return unAuthorized()

    def retrieve(self, request, pk=None):
        expense = self.get_object()
        return checkAndReturn(request.user, expense.project, "project_expenses_v",
                              expenseRetrieve(self, request, expense))

    def create(self, request):
        data = request.data
        try:
            project = Project.objects.only('id').get(pk=data['project'])
        except Project.DoesNotExist:
            return Response({"error": "Project does not exist!"}, status=status.HTTP_404_NOT_FOUND)
        return checkAndReturn(request.user, project, "project_expenses_c",
                              expernseCreate(self, request, data, project))

    def update(self, request, pk=None):
        expense = self.get_object()
        return checkAndReturn(request.user, expense.project, "project_expenses_u",
                              expenseUpdate(self, request, expense))

    @ action(detail=True, methods=["post"])
    def add_attachments(self, request, pk=None):
        try:
            expense = self.get_object()
            return checkAndReturn(request.user, expense.project, "expense_attachments_c",
                                  addAttachment(request, expense))
        except:
            return Response(
                {"message": "something went wrong"}, status=status.HTTP_400_BAD_REQUEST
            )

    @ action(detail=True, methods=["delete"])
    def delete_attachments(self, request, pk=None):
        expense = self.get_object()
        return checkAndReturn(request.user, expense.project, "expense_attachments_d",
                              deleteAttachments(self, request))

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
        return delete(self, request, Expense, permission="project_expenses_d")

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
