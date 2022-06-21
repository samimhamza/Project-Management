from common.permissions_scopes import (IncomePermissions, FocalPointPermissions,
                                       LocationPermissions, PaymentPermissions, StagePermissions, ProjectCategoryPermissions)
from common.actions import delete, allItems, filterRecords, addAttachment, deleteAttachments, getAttachments
from common.custom import CustomPageNumberPagination
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import viewsets, status
from projects.models import (
    Country,
    Location,
    FocalPoint,
    Income,
    Payment,
    State,
    Project,
    Stage,
    SubStage,
    ProjectCategory
)
from projects.api.serializers import (
    FocalPointSerializer,
    CountrySerializer,
    LocationSerializer,
    IncomeSerializer,
    PaymentSerializer,
    CountryListSerializer,
    StateListSerializer,
    StateSerializer,
    StageSerializer,
    StageListSerializer,
    ProjectCategorySerializer
)
from rest_framework import generics


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
            for data in serializer.data:
                data = getAttachments(
                    request, data, data['id'], 'income_attachments_v')
            return Response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        income = self.get_object()
        serializer = self.get_serializer(income)
        data = serializer.data
        data = getAttachments(
            request, data, data['id'], 'income_attachments_v')
        return Response(data)

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


class ProjectCategoryViewSet(viewsets.ModelViewSet):
    queryset = ProjectCategory.objects.all()
    serializer_class = ProjectCategorySerializer
    permission_classes = (ProjectCategoryPermissions,)
    pagination_class = CustomPageNumberPagination

    def list(self, request):
        queryset = self.get_queryset()
        queryset = filterRecords(queryset, request)
        if request.GET.get("items_per_page") == "-1":
            return allItems(ProjectCategorySerializer, queryset)
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)


class StageViewSet(viewsets.ModelViewSet):
    queryset = Stage.objects.all()
    serializer_class = StageSerializer
    permission_classes = (StagePermissions,)
    pagination_class = CustomPageNumberPagination

    def list(self, request):
        queryset = self.get_queryset()
        queryset = filterRecords(queryset, request)
        if request.GET.get("items_per_page") == "-1":
            return allItems(StageListSerializer, queryset)

        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)
