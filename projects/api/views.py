from common.permissions_scopes import (
    IncomePermissions, FocalPointPermissions, LocationPermissions, PaymentPermissions)
from common.actions import (allItems, filterRecords,
                            addAttachment, deleteAttachments, getAttachments, unAuthorized, checkProjectScope)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from common.Repository import Repository
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
from rest_framework import generics
from rest_framework import status
from datetime import datetime
from projects.models import (
    Country,
    Location,
    FocalPoint,
    Income,
    Payment,
    State,
    Project
)


def locationAction(self, project, data):
    location, created = Location.objects.get_or_create(project=project)
    location.address_line_one = data['address_line_one']
    location.address_line_two = data['address_line_two']
    location.city = data['city']
    try:
        if data["state_id"] is not None:
            state = State.objects.only('id').get(pk=data['state_id'])
        else:
            state = None
    except:
        state = None
    location.state = state
    location.save()

    try:
        if data["country_id"] is not None:
            country = Country.objects.only('id').get(pk=data['country_id'])
        else:
            country = None
    except Country.DoesNotExist:
        country = None
    state.country = country
    state.save()
    serializer = self.get_serializer(location)
    return Response(serializer.data, status=201)


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
        try:
            project = Project.objects.get(pk=data['project_id'])
        except Project.DoesNotExist:
            return Response({"error": "Project does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        if checkProjectScope(request.user, project, "projects_u"):
            return locationAction(self, project, data)
        else:
            return unAuthorized()


class MyLocationCreateAPIView(generics.CreateAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        data = request.data
        try:
            project = Project.objects.get(pk=data['project_id'])
        except Project.DoesNotExist:
            return Response({"error": "Project does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        if checkProjectScope(request.user, project, "projects_u"):
            return locationAction(self, project, data)
        else:
            return unAuthorized()


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
            date=datetime.now().date(),
            income=income,
            created_by=data["created_by"],
            updated_by=data["created_by"],
        )
        income.save()
        serializer = self.get_serializer(
            income)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


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


class FocalPointViewSet(Repository):
    model = FocalPoint
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
