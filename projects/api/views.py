from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
import datetime
from users.models import User
from projects.models import (
    Country,
    Location,
    FocalPoint,
    Income,
    Payment,
    Attachment,
)
from projects.api.serializers import (
    CountrySerializer,
    LocationSerializer,
    FocalPointSerializer,
    IncomeSerializer,
    PaymentSerializer,
    AttachmentSerializer,
)


class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer


class AttachmentViewSet(viewsets.ModelViewSet):
    queryset = Attachment.objects.all()
    serializer_class = AttachmentSerializer


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.filter(deleted_at__isnull=True)
    serializer_class = PaymentSerializer


class IncomeViewSet(viewsets.ModelViewSet):
    queryset = Income.objects.all()
    serializer_class = IncomeSerializer


class FocalPointViewSet(viewsets.ModelViewSet):
    queryset = FocalPoint.objects.all()
    serializer_class = FocalPointSerializer
