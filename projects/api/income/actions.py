from common.actions import getAttachments
from rest_framework.response import Response
from projects.models import Income, Payment
from rest_framework import status


def incomeList(self, request, queryset, project=None):
    queryset = queryset.filter(project=request.GET.get(
        "project_id")).order_by("-created_at")
    page = self.paginate_queryset(queryset)
    serializer = self.get_serializer(
        page, many=True, context={"request": request})
    for data in serializer.data:
        data = getAttachments(
            request, data, data['id'], 'income_attachments_v', project)
    return self.get_paginated_response(serializer.data)


def incomeRetrieve(self, request, income):
    serializer = self.get_serializer(income, context={"request": request})
    data = serializer.data
    data = getAttachments(
        request, data, data['id'], 'income_attachments_v', income.project)
    return Response(data)


def incomeCreate(self, request, data, project):
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


def incomeUpdate(self, request, income):
    for key, value in request.data.items():
        setattr(income, key, value)
    income.updated_by = request.user
    income.save()
    serializer = self.get_serializer(income, context={"request": request})
    return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


def paymentCreate(self, data, income):
    payment = Payment.objects.create(
        source=data["source"],
        amount=data["amount"],
        date=data["date"],
        payment_method=data["payment_method"],
        income=income,
        created_by=data["created_by"],
        updated_by=data["created_by"],
    )
    payment.save()
    serializer = self.get_serializer(
        payment)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


def paymentUpdate(self, request, payment):
    for key, value in request.data.items():
        setattr(payment, key, value)
    payment.updated_by = request.user
    payment.save()
    serializer = self.get_serializer(payment, context={"request": request})
    return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
