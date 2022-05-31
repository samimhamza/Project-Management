from urllib import response
from rest_framework import viewsets
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
from common.custom import CustomPageNumberPagination
from rest_framework.response import Response


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
    # queryset = Income.objects.all()
    queryset = Income.objects.filter(
        deleted_at__isnull=True).order_by("-created_at")
    serializer_class = IncomeSerializer
    # pagination_class = CustomPageNumberPagination

    def list(self, request):
        queryset = self.get_queryset()
        if request.GET.get("project_id"):
            queryset = Income.objects.filter(
            deleted_at__isnull=True, project=request.GET.get("project_id")).order_by("-created_at")
            # page = self.paginate_queryset(queryset)
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)

        # page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)



class FocalPointViewSet(viewsets.ModelViewSet):
    queryset = FocalPoint.objects.all()
    serializer_class = FocalPointSerializer
