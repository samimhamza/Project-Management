from common.actions import allItems, filterRecords, delete, allItems, restore, trashList, withTrashed
from .serializers import DepartmentSerializer, DepartmentTrashedSerializer
from common.permissions_scopes import DepartmentPermissions
from common.custom import CustomPageNumberPagination
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import viewsets, status
from projects.models import Department


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.filter(
        deleted_at__isnull=True).order_by('-updated_at')
    serializer_class = DepartmentSerializer
    permission_classes = (DepartmentPermissions,)
    pagination_class = CustomPageNumberPagination
    serializer_action_classes = {
        "trashed": DepartmentTrashedSerializer,
    }

    def list(self, request):
        queryset = self.get_queryset()
        queryset = filterRecords(queryset, request)
        if request.GET.get("items_per_page") == "-1":
            return allItems(DepartmentSerializer, queryset)
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    def create(self, request):
        data = request.data
        data["created_by"] = request.user
        new_category = Department.objects.create(
            name=data["name"],
            created_by=data["created_by"],
            updated_by=data["created_by"],
        )
        new_category.save()
        serializer = self.get_serializer(
            new_category)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        project = self.get_object()
        data = request.data
        for key, value in data.items():
            if key != "id":
                setattr(project, key, value)
        project.updated_by = request.user
        project.save()
        serializer = self.get_serializer(
            project)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def destroy(self, request, pk=None):
        return delete(self, request, Department)

    @ action(detail=False, methods=["get"])
    def all(self, request):
        return withTrashed(self, Department, order_by="-created_at")

    @ action(detail=False, methods=["get"])
    def trashed(self, request):
        return trashList(self, Department)

    # for multi and single restore
    @ action(detail=False, methods=["put"])
    def restore(self, request, pk=None):
        return restore(self, request, Department)

    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()
