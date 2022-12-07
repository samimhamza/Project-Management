from projects.api.department.serializers import (
    StageListSerializer, SubStageListSerializer, StageTrashedSerializer, SubStageTrashedSerializer)
from common.permissions_scopes import StagePermissions, SubStagePermissions
from common.actions import allItems, filterRecords
from rest_framework.response import Response
from projects.models import Stage, SubStage
from common.Repository import Repository
from projects.models import Department
from rest_framework import status


class StageViewSet(Repository):
    model = Stage
    queryset = Stage.objects.filter(
        deleted_at__isnull=True).order_by('-updated_at')
    serializer_class = StageListSerializer
    permission_classes = (StagePermissions,)
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
        if "description" in data:
            description = data["description"]
        else:
            description = None
        new_stage = Stage.objects.create(
            name=data["name"],
            description=description,
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
        if "department" in data:
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


class SubStageViewSet(Repository):
    model = SubStage
    queryset = SubStage.objects.filter(
        deleted_at__isnull=True).order_by('-updated_at')
    serializer_class = SubStageListSerializer
    permission_classes = (SubStagePermissions,)
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
        if "description" in data:
            description = data["description"]
        else:
            description = None
        new_stage = SubStage.objects.create(
            name=data["name"],
            description=description,
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
