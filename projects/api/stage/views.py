from .serializers import (StageSerializer, StageListSerializer, SubStageSerializer,
                          SubStageListSerializer, StageTrashedSerializer, SubStageTrashedSerializer)
from common.actions import allItems, filterRecords, delete, trashList, withTrashed, restore
from common.permissions_scopes import StagePermissions, SubStagePermissions
from common.custom import CustomPageNumberPagination
from rest_framework.decorators import action
from projects.models import Stage, SubStage
from rest_framework import viewsets


class StageViewSet(viewsets.ModelViewSet):
    queryset = Stage.objects.all()
    serializer_class = StageSerializer
    permission_classes = (StagePermissions,)
    pagination_class = CustomPageNumberPagination
    serializer_action_classes = {
        "trashed": StageTrashedSerializer
    }

    def list(self, request):
        queryset = self.get_queryset()
        queryset = filterRecords(queryset, request)
        if request.GET.get("items_per_page") == "-1":
            return allItems(StageListSerializer, queryset)

        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    def destroy(self, request, pk=None):
        return delete(self, request, Stage)

    @action(detail=False, methods=["get"])
    def all(self, request):
        return withTrashed(self, Stage, order_by="-created_at")

    @action(detail=False, methods=["get"])
    def trashed(self, request):
        return trashList(self, Stage)

    # for multi and single restore
    @action(detail=False, methods=["get"])
    def restore(self, request, pk=None):
        return restore(self, request, Stage)

    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()


class SubStageViewSet(viewsets.ModelViewSet):
    queryset = SubStage.objects.all()
    serializer_class = SubStageSerializer
    permission_classes = (SubStagePermissions,)
    pagination_class = CustomPageNumberPagination
    serializer_action_classes = {
        "trashed": SubStageTrashedSerializer
    }

    def list(self, request):
        queryset = self.get_queryset()
        queryset = filterRecords(queryset, request)
        if request.GET.get("items_per_page") == "-1":
            return allItems(SubStageListSerializer, queryset)

        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    def destroy(self, request, pk=None):
        return delete(self, request, SubStage)

    @action(detail=False, methods=["get"])
    def all(self, request):
        return withTrashed(self, SubStage, order_by="-created_at")

    @action(detail=False, methods=["get"])
    def trashed(self, request):
        return trashList(self, SubStage)

    # for multi and single restore
    @action(detail=False, methods=["get"])
    def restore(self, request, pk=None):
        return restore(self, request, SubStage)

    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()
