from common.actions import filterRecords, addAttachment, deleteAttachments, getAttachments
from common.permissions_scopes import IncomePermissions, PaymentPermissions
from rest_framework.response import Response
from rest_framework.decorators import action
from common.Repository import Repository
from projects.api.serializers import (
    IncomeSerializer,
    PaymentSerializer,
    IncomeTrashedSerializer,
    PaymentTrashedSerializer
)
from rest_framework import status
from projects.models import (
    Income,
    Payment,
    Project
)


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
        income = Payment.objects.create(
            source=data["source"],
            amount=data["amount"],
            date=data["date"],
            payment_method=data["payment_method"],
            income=income,
            created_by=data["created_by"],
            updated_by=data["created_by"],
        )
        income.save()
        serializer = self.get_serializer(
            income)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        payment = self.get_object()
        for key, value in request.data.items():
            setattr(payment, key, value)
        payment.updated_by = request.user
        payment.save()
        serializer = self.get_serializer(payment, context={"request": request})
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


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
            queryset = queryset.filter(project=request.GET.get(
                "project_id")).order_by("-created_at")
            page = self.paginate_queryset(queryset)
            serializer = self.get_serializer(
                page, many=True, context={"request": request})
            for data in serializer.data:
                data = getAttachments(
                    request, data, data['id'], 'income_attachments_v')
            return self.get_paginated_response(serializer.data)
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(
            page, many=True, context={"request": request})
        return self.get_paginated_response(serializer.data)

    def retrieve(self, request, pk=None):
        income = self.get_object()
        serializer = self.get_serializer(income, context={"request": request})
        data = serializer.data
        data = getAttachments(
            request, data, data['id'], 'income_attachments_v')
        return Response(data)

    def create(self, request):
        data = request.data
        data["created_by"] = request.user
        try:
            project = Project.objects.get(pk=data["project"])
        except Project.DoesNotExist:
            return Response({"error": "Project does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        income = Income.objects.create(
            title=data["title"],
            type=data["type"],
            amount=data["amount"],
            date=data["date"],
            project=project,
            created_by=data["created_by"],
            updated_by=data["created_by"],
        )
        income.save()
        serializer = self.get_serializer(
            income, context={"request": request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

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
