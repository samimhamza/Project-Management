from .serializers import StageSerializer, StageListSerializer, SubStageSerializer, SubStageListSerializer
from common.permissions_scopes import StagePermissions, SubStagePermissions
from common.custom import CustomPageNumberPagination
from common.actions import allItems, filterRecords
from projects.models import Stage, SubStage
from rest_framework import viewsets


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


class SubStageViewSet(viewsets.ModelViewSet):
    queryset = SubStage.objects.all()
    serializer_class = SubStageSerializer
    permission_classes = (SubStagePermissions,)
    pagination_class = CustomPageNumberPagination

    def list(self, request):
        queryset = self.get_queryset()
        queryset = filterRecords(queryset, request)
        if request.GET.get("items_per_page") == "-1":
            return allItems(SubStageListSerializer, queryset)

        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)
