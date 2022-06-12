from common.permissions_scopes import (IncomePermissions,
                                       FocalPointPermissions, LocationPermissions, PaymentPermissions)
from common.actions import delete, allItems, filterRecords
from rest_framework.response import Response
from rest_framework import viewsets, status
from projects.models import (
    Country,
    Location,
    FocalPoint,
    Income,
    Payment,
    State,
    Project
)
from projects.api.serializers import (
    FocalPointSerializer,
    CountrySerializer,
    LocationSerializer,
    IncomeSerializer,
    PaymentSerializer,
    CountryListSerializer,
    StateListSerializer,
    StateSerializer

)
from rest_framework import generics
import pusher


class CountryListAPIView(generics.ListAPIView):
    queryset = Country.objects.all().order_by('name')
    serializer_class = CountrySerializer

    def list(self, request):
        queryset = self.get_queryset()
        queryset = filterRecords(queryset, request)
        if request.GET.get("items_per_page") == "-1":
            return allItems(CountryListSerializer, queryset)
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)


class StateListAPIView(generics.ListAPIView):
    queryset = State.objects.all().order_by('name')
    serializer_class = StateSerializer

    def list(self, request):
        queryset = self.get_queryset()
        queryset = filterRecords(queryset, request)
        if request.GET.get("items_per_page") == "-1":
            return allItems(StateListSerializer, queryset)
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)


class LocationCreateAPIView(generics.CreateAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = (LocationPermissions,)

    def post(self, request, *args, **kwargs):
        data = request.data
        project = Project.objects.get(pk=data['project_id'])
        location, created = Location.objects.get_or_create(project=project)
        location.address_line_one = data['address_line_one']
        location.address_line_two = data['address_line_two']
        location.city = data['city']
        state = State.objects.only('id').get(pk=data['state_id'])
        location.state = state
        location.save()
        country = Country.objects.only('id').get(pk=data['country_id'])
        state.country = country
        state.save()
        serializer = self.get_serializer(location)
        return Response(serializer.data, status=201)


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

    def list(self, request):
        queryset = self.get_queryset()
        if request.GET.get("project_id"):
            queryset = FocalPoint.objects.filter(
                deleted_at__isnull=True, project=request.GET.get("project_id")).order_by("-created_at")
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
