from common.permissions_scopes import FocalPointPermissions, LocationPermissions
from common.actions import (allItems, filterRecords, unAuthorized, checkAndReturn,
                            checkProjectScope, convertBase64ToImage, delete)
from projects.actions import focalPointCreate, focalPointList, focalPointUpdate
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, viewsets
from common.Repository import Repository
from projects.api.serializers import (
    FocalPointSerializer,
    CountrySerializer,
    LocationSerializer,
    CountryListSerializer,
    StateListSerializer,
    StateSerializer,
    FocalPointTrashedSerializer,
)
from rest_framework import generics
from projects.models import (
    Country,
    Location,
    FocalPoint,
    State,
    Project
)
import os


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
            return focalPointList(self, request, queryset)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        data = request.data
        try:
            project = Project.objects.only(
                'id').get(pk=data["project"])
        except Project.DoesNotExist:
            return Response({"error": "Project does not exist!"}, status=status.HTTP_404_NOT_FOUND)
        return focalPointCreate(self, request, data, project)

    def update(self, request, pk=None):
        focal_point = self.get_object()
        return focalPointUpdate(self, request, focal_point)

    def destroy(self, request, pk=None):
        return delete(self, request, FocalPoint, imageField="profile")


class MyFocalPointViewSet(viewsets.ModelViewSet):
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
            try:
                project = Project.objects.get(pk=request.GET.get("project_id"))
            except Project.DoesNotExist:
                return unAuthorized()
            if checkProjectScope(request.user, project, "project_focal_points_v"):
                queryset = self.get_queryset()
                return focalPointList(self, request, queryset)
            else:
                return unAuthorized()
        else:
            return unAuthorized()

    def create(self, request):
        data = request.data
        try:
            project = Project.objects.only(
                'id').get(pk=data["project"])
        except Project.DoesNotExist:
            return Response({"error": "Project does not exist!"}, status=status.HTTP_404_NOT_FOUND)
        return checkAndReturn(request.user, project, "project_focal_points_c",
                              focalPointCreate(self, request, data, project))

    def update(self, request, pk=None):
        focal_point = self.get_object()
        return checkAndReturn(request.user, focal_point.project, "project_focal_points_u",
                              focalPointUpdate(self, request, focal_point))

    def destroy(self, request, pk=None):
        return delete(self, request, FocalPoint, imageField="profile", permission="project_focal_points_d")
