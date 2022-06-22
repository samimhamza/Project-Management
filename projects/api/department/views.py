from common.permissions_scopes import DepartmentPermissions
from .serializers import DepartmentSerializer
from common.custom import CustomPageNumberPagination
from common.actions import allItems, filterRecords
from rest_framework.response import Response
from rest_framework import viewsets, status
from projects.models import Department


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = (DepartmentPermissions,)
    pagination_class = CustomPageNumberPagination

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
