from common.actions import (delete, allItems, filterRecords, addAttachment,
                            deleteAttachments, getAttachments, restore, withTrashed, trashList)
from common.permissions_scopes import (
    IncomePermissions, FocalPointPermissions, LocationPermissions, PaymentPermissions)
from common.custom import CustomPageNumberPagination
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import viewsets, status
from rest_framework import generics
from projects.api.serializers import (
    FocalPointSerializer,
    CountrySerializer,
    LocationSerializer,
    IncomeSerializer,
    PaymentSerializer,
    CountryListSerializer,
    StateListSerializer,
    StateSerializer,
    FocalPointTrashedSerializer,
    IncomeTrashedSerializer,
    PaymentTrashedSerializer
)
from projects.models import (
    Country,
    Location,
    FocalPoint,
    Income,
    Payment,
    State,
    Project
)


class CountryListAPIView(generics.ListAPIView):
    queryset = Country.objects.all().order_by('name')
    serializer_class = CountrySerializer

    def list(self, request):
        queryset = self.get_queryset()
        queryset = filterRecords(queryset, request, table=Country)
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
        queryset = filterRecords(queryset, request, table=State)
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
    serializer_action_classes = {
        "trashed": PaymentTrashedSerializer
    }

    @action(detail=False, methods=["get"])
    def all(self, request):
        return withTrashed(self, Payment, order_by="-created_at")

    @action(detail=False, methods=["get"])
    def trashed(self, request):
        return trashList(self, Payment)

    # for multi and single restore
    @action(detail=False, methods=["put"])
    def restore(self, request, pk=None):
        return restore(self, request, Payment)

    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()


class IncomeViewSet(viewsets.ModelViewSet):
    queryset = Income.objects.filter(
        deleted_at__isnull=True).order_by("-created_at")
    serializer_class = IncomeSerializer
    permission_classes = (IncomePermissions,)
    pagination_class = CustomPageNumberPagination
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
            serializer = self.get_serializer(page, many=True)
            for data in serializer.data:
                data = getAttachments(
                    request, data, data['id'], 'income_attachments_v')
            return self.get_paginated_response(serializer.data)
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    def retrieve(self, request, pk=None):
        income = self.get_object()
        serializer = self.get_serializer(income)
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
            income)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        income = self.get_object()
        for key, value in request.data.items():
            setattr(income, key, value)
        income.updated_by = request.user
        income.save()
        serializer = IncomeSerializer(income)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def destroy(self, request, pk=None):
        return delete(self, request, Income)

    @action(detail=True, methods=["post"])
    def add_attachments(self, request, pk=None):
        return addAttachment(self, request)

    @action(detail=True, methods=["delete"])
    def delete_attachments(self, request, pk=None):
        return deleteAttachments(self, request)

    @action(detail=False, methods=["get"])
    def all(self, request):
        return withTrashed(self, Income, order_by="-created_at")

    @action(detail=False, methods=["get"])
    def trashed(self, request):
        return trashList(self, Income)

    # for multi and single restore
    @action(detail=False, methods=["put"])
    def restore(self, request, pk=None):
        return restore(self, request, Income)

    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()


class FocalPointViewSet(viewsets.ModelViewSet):
    queryset = FocalPoint.objects.all()
    serializer_class = FocalPointSerializer
    permission_classes = (FocalPointPermissions,)
    serializer_action_classes = {
        "trashed": FocalPointTrashedSerializer
    }

    def list(self, request):
        queryset = self.get_queryset()
        if request.GET.get("project_id"):
            queryset = FocalPoint.objects.filter(
                deleted_at__isnull=True, project=request.GET.get("project_id")).order_by("-created_at")
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def all(self, request):
        return withTrashed(self, FocalPoint, order_by="-created_at")

    @action(detail=False, methods=["get"])
    def trashed(self, request):
        return trashList(self, FocalPoint)

    # for multi and single restore
    @action(detail=False, methods=["put"])
    def restore(self, request, pk=None):
        return restore(self, request, FocalPoint)

    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()
