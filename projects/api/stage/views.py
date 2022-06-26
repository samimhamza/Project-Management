from .serializers import (StageSerializer, StageListSerializer, SubStageSerializer,
                          SubStageListSerializer, StageTrashedSerializer, SubStageTrashedSerializer)
from common.actions import allItems, filterRecords, delete, trashList, withTrashed, restore
from common.permissions_scopes import StagePermissions, SubStagePermissions
from common.custom import CustomPageNumberPagination
from rest_framework.response import Response
from rest_framework.decorators import action
from projects.models import Stage, SubStage
from rest_framework import viewsets, status
from projects.models import Department


class StageViewSet(viewsets.ModelViewSet):
    queryset = Stage.objects.filter(
        deleted_at__isnull=True).order_by('-updated_at')
    serializer_class = StageSerializer
    permission_classes = (StagePermissions,)
    pagination_class = CustomPageNumberPagination
    serializer_action_classes = {
        "trashed": StageTrashedSerializer
    }

    def list(self, request):
        queryset = self.get_queryset()
        queryset = filterRecords(queryset, request, table=Stage)
        if request.GET.get("items_per_page") == "-1":
            return allItems(StageListSerializer, queryset)

        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    def create(self, request):
        data = request.data
        data["created_by"] = request.user
        try:
            depratment = Department.objects.only(
                'id').get(pk=data["department"])
        except Department.DoesNotExist:
            return Response({"error": "Department does not exist!"}, status=status.HTTP_404_NOT_FOUND)

        new_stage = Stage.objects.create(
            name=data["name"],
            description=data["description"],
            created_by=data["created_by"],
            updated_by=data["created_by"],
            department=depratment
        )
        new_stage.save()
        serializer = self.get_serializer(new_stage)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        stage = self.get_object()
        data = request.data
        try:
            depratment = Department.objects.only(
                'id').get(pk=data["department"])
        except Department.DoesNotExist:
            return Response({"error": "Department does not exist!"}, status=status.HTTP_404_NOT_FOUND)
        stage.department = depratment
        for key, value in data.items():
            if key != "id":
                setattr(stage, key, value)
        stage.updated_by = request.user
        stage.save()
        serializer = self.get_serializer(stage)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def destroy(self, request, pk=None):
        return delete(self, request, Stage)

    @action(detail=False, methods=["get"])
    def all(self, request):
        return withTrashed(self, Stage, order_by="-created_at")

    @action(detail=False, methods=["get"])
    def trashed(self, request):
        return trashList(self, Stage)

    # for multi and single restore
    @action(detail=False, methods=["put"])
    def restore(self, request, pk=None):
        return restore(self, request, Stage)

    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()


class SubStageViewSet(viewsets.ModelViewSet):
    queryset = SubStage.objects.filter(
        deleted_at__isnull=True).order_by('-updated_at')
    serializer_class = SubStageSerializer
    permission_classes = (SubStagePermissions,)
    pagination_class = CustomPageNumberPagination
    serializer_action_classes = {
        "trashed": SubStageTrashedSerializer
    }

    def list(self, request):
        queryset = self.get_queryset()
        queryset = filterRecords(queryset, request, table=SubStage)
        if request.GET.get("items_per_page") == "-1":
            return allItems(SubStageListSerializer, queryset)

        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    def create(self, request):
        data = request.data
        data["created_by"] = request.user
        try:
            stage = Stage.objects.only(
                'id').get(pk=data["stage"])
        except Stage.DoesNotExist:
            return Response({"error": "Stage does not exist!"}, status=status.HTTP_404_NOT_FOUND)

        new_stage = SubStage.objects.create(
            name=data["name"],
            description=data["description"],
            created_by=data["created_by"],
            updated_by=data["created_by"],
            stage=stage
        )
        new_stage.save()
        serializer = self.get_serializer(new_stage)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        subStage = self.get_object()
        data = request.data
        if "stage" in data:
            try:
                parent = Stage.objects.only(
                    'id').get(pk=data["stage"])
                subStage.stage = parent
            except Stage.DoesNotExist:
                return Response({"error": "Stage does not exist!"}, status=status.HTTP_404_NOT_FOUND)

        for key, value in data.items():
            if key != "id":
                setattr(subStage, key, value)
        subStage.updated_by = request.user
        subStage.save()
        serializer = self.get_serializer(subStage)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def destroy(self, request, pk=None):
        return delete(self, request, SubStage)

    @action(detail=False, methods=["get"])
    def all(self, request):
        return withTrashed(self, SubStage, order_by="-created_at")

    @action(detail=False, methods=["get"])
    def trashed(self, request):
        return trashList(self, SubStage)

    # for multi and single restore
    @action(detail=False, methods=["put"])
    def restore(self, request, pk=None):
        return restore(self, request, SubStage)

    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()
