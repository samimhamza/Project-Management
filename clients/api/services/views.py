from .serializers import ServiceSerializer, ServiceListSerializer
from common.custom import CustomPageNumberPagination
from common.actions import filterRecords, allItems
from rest_framework.response import Response
from rest_framework import viewsets
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
