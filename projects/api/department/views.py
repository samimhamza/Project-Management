from .serializers import DepartmentSerializer, DepartmentTrashedSerializer
from common.actions import allItems, filterRecords, allItems
from common.permissions_scopes import DepartmentPermissions
from rest_framework.response import Response
from common.Repository import Repository
from projects.models import Department
from rest_framework import status


class DepartmentViewSet(Repository):
    model = Department
    queryset = Department.objects.filter(
        deleted_at__isnull=True).order_by('-updated_at')
    serializer_class = DepartmentSerializer
    permission_classes = (DepartmentPermissions,)
    serializer_action_classes = {
        "trashed": DepartmentTrashedSerializer,
    }

    def list(self, request):
        queryset = self.get_queryset()
        queryset = filterRecords(queryset, request, table=Department)
        if request.GET.get("items_per_page") == "-1":
            return allItems(DepartmentSerializer, queryset)
        if request.GET.get("items_per_page") == "-2":
            return allItems(self.get_serializer, queryset)
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    def create(self, request):
        data = request.data
        data["created_by"] = request.user
        if "description" in data:
            description = data["description"]
        else:
            description = None
        new_category = Department.objects.create(
            name=data["name"],
            description=description,
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
