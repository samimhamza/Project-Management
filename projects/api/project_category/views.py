from common.permissions_scopes import ProjectCategoryPermissions
from .serializers import ProjectCategorySerializer
from common.custom import CustomPageNumberPagination
from common.actions import allItems, filterRecords
from rest_framework.response import Response
from rest_framework import viewsets, status
from projects.models import ProjectCategory


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

    def create(self, request):
        data = request.data
        if request.data.get("parent"):
            parent = ProjectCategory.objects.only('id').get(pk=data['parent'])
        else:
            parent = None
        data["created_by"] = request.user
        new_category = ProjectCategory.objects.create(
            parent=parent,
            name=data["name"],
            created_by=data["created_by"],
            updated_by=data["created_by"],
        )
        new_category.save()
        serializer = self.get_serializer(
            new_category)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
