from common.permissions_scopes import (AttachmentPermissions, IncomePermissions,
                                       FocalPointPermissions, LocationPermissions, PaymentPermissions)                                 
from common.actions import delete                                       
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
from rest_framework.response import Response
from rest_framework import viewsets, status
import pusher


class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer


class AttachmentViewSet(viewsets.ModelViewSet):
    queryset = Attachment.objects.all()
    serializer_class = AttachmentSerializer
    permission_classes = (AttachmentPermissions,)


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = (LocationPermissions,)


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.filter(deleted_at__isnull=True)
    serializer_class = PaymentSerializer
    permission_classes = (PaymentPermissions,)


class IncomeViewSet(viewsets.ModelViewSet):
    queryset = Income.objects.filter(
        deleted_at__isnull=True).order_by("-created_at")
    serializer_class = IncomeSerializer
    permission_classes = (IncomePermissions,)

    def list(self, request):
        queryset = self.get_queryset()
        if request.GET.get("project_id"):
            queryset = Income.objects.filter(
                deleted_at__isnull=True, project=request.GET.get("project_id")).order_by("-created_at")
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)

        # pusher_client = pusher.Pusher(
        #     app_id='1419045',
        #     key='237907cedac4eed704cd',
        #     secret='2afd20009cf5404d0df6',
        #     cluster='ap2',
        #     ssl=True
        # )
        # pusher_client.trigger('my-channel', 'my-event', {'message': 'hello world Django'})

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def update(self, request, pk=None):
        income = self.get_object()
        if request.data.get("title"):
            income.title = request.data.get("title")
        if request.data.get("description"):
            income.description = request.data.get("description")
        if request.data.get("type"):
            income.type = request.data.get("type")
        if request.data.get("amount"):
            income.amount = request.data.get("amount")
        income.updated_by = request.user
        income.save()
        serializer = IncomeSerializer(income)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def destroy(self, request, pk=None):
        return delete(self, request, Income)


class FocalPointViewSet(viewsets.ModelViewSet):
    queryset = FocalPoint.objects.all()
    serializer_class = FocalPointSerializer
    permission_classes = (FocalPointPermissions,)
