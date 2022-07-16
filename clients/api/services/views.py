from .serializers import ServiceSerializer, ServiceListSerializer
from common.custom import CustomPageNumberPagination
from common.actions import filterRecords, allItems
from rest_framework.response import Response
from rest_framework import viewsets, status
from clients.models import Service


class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.filter(
        deleted_at__isnull=True).order_by("-created_at")
    serializer_class = ServiceSerializer
    pagination_class = CustomPageNumberPagination

    def list(self, request):
        queryset = self.get_queryset()
        queryset = filterRecords(queryset, request, table=Service)
        if request.GET.get("items_per_page") == "-1":
            return allItems(ServiceListSerializer, queryset)

        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    def create(self, request):
        data = request.data
        creator = request.user
        if request.data.get("parent"):
            parent = Service.objects.only('id').get(pk=data['parent'])
        else:
            parent = None
        new_service = Service.objects.create(
            parent=parent,
            name=data['name'],
            description=data["description"],
            created_by=creator,
            updated_by=creator,
        )
        new_service.save()
        serializer = self.get_serializer(new_service)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        service = self.get_object()
        if "parent" in request.data:
            parent = Service.objects.only('id').get(pk=request.data['parent'])
            service.parent = parent
        for key, value in request.data.items():
            if key != "parent":
                setattr(service, key, value)
        service.updated_by = request.user
        service.save()
        serializer = self.get_serializer(service)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
