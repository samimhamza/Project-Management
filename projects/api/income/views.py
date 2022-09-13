from common.actions import (filterRecords, addAttachment, deleteAttachments, checkAndReturn,
                            checkProjectScope, unAuthorized, delete)
from .actions import (incomeCreate, paymentUpdate,
                      incomeList, incomeRetrieve, incomeUpdate, paymentCreate)
from common.permissions_scopes import IncomePermissions, PaymentPermissions
from rest_framework.permissions import IsAuthenticated
from common.custom import CustomPageNumberPagination
from rest_framework.response import Response
from rest_framework.decorators import action
from common.Repository import Repository
from projects.api.serializers import (
    IncomeSerializer,
    PaymentSerializer,
    IncomeTrashedSerializer,
    PaymentTrashedSerializer
)
from rest_framework import status, viewsets
from projects.models import (
    Income,
    Payment,
    Project
)


class IncomeViewSet(Repository):
    model = Income
    queryset = Income.objects.filter(
        deleted_at__isnull=True).order_by("-created_at")
    serializer_class = IncomeSerializer
    permission_classes = (IncomePermissions,)
    serializer_action_classes = {
        "trashed": IncomeTrashedSerializer
    }

    def list(self, request):
        queryset = self.get_queryset()
        queryset = filterRecords(queryset, request, table=Income)
        if request.GET.get("project_id"):
            return incomeList(self, request, queryset)
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(
            page, many=True, context={"request": request})
        return self.get_paginated_response(serializer.data)

    def retrieve(self, request, pk=None):
        income = self.get_object()
        return incomeRetrieve(self, request, income)

    def create(self, request):
        data = request.data
        data["created_by"] = request.user
        try:
            project = Project.objects.get(pk=data["project"])
        except Project.DoesNotExist:
            return Response({"error": "Project does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        return incomeCreate(self, request, data, project)

    def update(self, request, pk=None):
        income = self.get_object()
        for key, value in request.data.items():
            setattr(income, key, value)
        income.updated_by = request.user
        income.save()
        serializer = self.get_serializer(income, context={"request": request})
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    @action(detail=True, methods=["post"])
    def add_attachments(self, request, pk=None):
        try:
            income = self.get_object()
            return addAttachment(request, income)
        except:
            return Response(
                {"message": "something went wrong"}, status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=["delete"])
    def delete_attachments(self, request, pk=None):
        return deleteAttachments(self, request)


class PaymentViewSet(Repository):
    model = Payment
    queryset = Payment.objects.filter(deleted_at__isnull=True)
    serializer_class = PaymentSerializer
    permission_classes = (PaymentPermissions,)
    serializer_action_classes = {
        "trashed": PaymentTrashedSerializer
    }

    def create(self, request):
        data = request.data
        data["created_by"] = request.user
        try:
            income = Income.objects.get(pk=data["income"])
        except Income.DoesNotExist:
            return Response({"error": "Income does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        return paymentCreate(self, data, income)

    def update(self, request, pk=None):
        payment = self.get_object()
        return paymentUpdate(self, request, payment)


class MyIncomeViewSet(viewsets.ModelViewSet):
    queryset = Income.objects.filter(
        deleted_at__isnull=True).order_by("-created_at")
    pagination_class = CustomPageNumberPagination
    serializer_class = IncomeSerializer
    permission_classes = (IsAuthenticated,)
    serializer_action_classes = {
        "trashed": IncomeTrashedSerializer
    }

    def list(self, request):
        if request.GET.get("project_id"):
            try:
                project = Project.objects.get(pk=request.GET.get("project_id"))
            except Project.DoesNotExist:
                return unAuthorized()
            if checkProjectScope(request.user, project, "project_incomes_v"):
                queryset = self.get_queryset()
                queryset = filterRecords(queryset, request, table=Income)
                return incomeList(self, request, queryset, project)
            else:
                return unAuthorized()
        else:
            return unAuthorized()

    def retrieve(self, request, pk=None):
        income = self.get_object()
        return checkAndReturn(request.user, income.project, "project_incomes_v",
                              incomeRetrieve(self, request, income))

    def create(self, request):
        data = request.data
        data["created_by"] = request.user
        try:
            project = Project.objects.get(pk=data["project"])
        except Project.DoesNotExist:
            return Response({"error": "Project does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        return checkAndReturn(request.user, project, "project_incomes_c",
                              incomeCreate(self, request, data, project))

    def update(self, request, pk=None):
        income = self.get_object()
        return checkAndReturn(request.user, income.project, "project_incomes_u",
                              incomeUpdate(self, request, income))

    @action(detail=True, methods=["post"])
    def add_attachments(self, request, pk=None):
        try:
            income = self.get_object()
            return checkAndReturn(request.user, income.project, "income_attachments_c",
                                  addAttachment(request, income))
        except:
            return Response(
                {"message": "something went wrong"}, status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=["delete"])
    def delete_attachments(self, request, pk=None):
        income = self.get_object()
        return checkAndReturn(request.user, income.project, "income_attachments_d",
                              deleteAttachments(self, request))

    def destroy(self, request, pk=None):
        return delete(self, request, Income, permission="project_incomes_d")

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


class MyPaymentViewSet(viewsets.ModelViewSet):
    model = Payment
    queryset = Payment.objects.filter(deleted_at__isnull=True)
    serializer_class = PaymentSerializer
    permission_classes = (IsAuthenticated,)
    serializer_action_classes = {
        "trashed": PaymentTrashedSerializer
    }

    def list(self, request):
        return Response([])

    def retrieve(self, request, pk=None):
        if request.GET.get("project_id"):
            try:
                project = Project.objects.get(pk=request.GET.get("project_id"))
            except Project.DoesNotExist:
                return unAuthorized()
            if checkProjectScope(request.user, project, "project_incomes_v"):
                payment = Payment.objects.get(pk=pk)
                serializer = self.get_serializer(payment)
                return Response(serializer.data)
            else:
                return unAuthorized()
        else:
            return unAuthorized()

    def create(self, request):
        data = request.data
        data["created_by"] = request.user
        try:
            income = Income.objects.get(pk=data["income"])
        except Income.DoesNotExist:
            return Response({"error": "Income does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        return checkAndReturn(request.user, income.project, "project_incomes_c",
                              paymentCreate(self, data, income))

    def update(self, request, pk=None):
        payment = self.get_object()
        return checkAndReturn(request.user, payment.income.project, "project_incomes_u",
                              paymentUpdate(self, request, payment))

    def destroy(self, request, pk=None):
        return delete(self, request, Payment, permission="project_incomes_d", specialCase='income')

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
