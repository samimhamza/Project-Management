from common.permissions_scopes import FocalPointPermissions, LocationPermissions
from common.actions import (allItems, filterRecords, unAuthorized,
                            checkProjectScope, convertBase64ToImage, delete)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
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
from rest_framework import status
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
            queryset = FocalPoint.objects.filter(
                deleted_at__isnull=True, project=request.GET.get("project_id")).order_by("-created_at")
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        data = request.data
        data["created_by"] = request.user
        try:
            project = Project.objects.only(
                'id').get(pk=data["project"])
        except Project.DoesNotExist:
            return Response({"error": "Project does not exist!"}, status=status.HTTP_404_NOT_FOUND)
        profile = convertBase64ToImage(data["profile"])
        new_focalPoint = FocalPoint.objects.create(
            project=project,
            profile=profile,
            contact_name=data["contact_name"],
            contact_last_name=data["contact_last_name"],
            phone=data["phone"],
            email=data["email"],
            whatsapp=data["whatsapp"],
            position=data["position"],
            prefer_communication_way=data["prefer_communication_way"],
            created_by=data["created_by"],
            updated_by=data["created_by"],
        )
        new_focalPoint.save()
        serializer = self.get_serializer(
            new_focalPoint, context={"request": request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        focal_point = self.get_object()
        data = request.data
        if request.data.get("project"):
            try:
                project = Project.objects.only(
                    'id').get(pk=data["project"])
            except Project.DoesNotExist:
                return Response({"error": "Project does not exist!"}, status=status.HTTP_404_NOT_FOUND)
            focal_point.project = project
        if request.data.get("profile"):
            imageField = convertBase64ToImage(data["profile"])
            if imageField:
                if os.path.isfile('media/'+str(focal_point.profile)):
                    os.remove('media/'+str(focal_point.profile))
                focal_point.profile = imageField
        for key, value in data.items():
            if key != "id" and key != "project" and key != "profile":
                setattr(focal_point, key, value)
        focal_point.updated_by = request.user
        focal_point.save()
        serializer = self.get_serializer(
            focal_point, context={"request": request})
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def destroy(self, request, pk=None):
        return delete(self, request, FocalPoint, imageField="profile")
