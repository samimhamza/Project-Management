from common.actions import (withTrashed, trashList, delete,
                            restore, clientFeaturesFormatter, clientServicesFormatter, filterRecords, allItems)
from .serializers import ClientSerializer, ClientDetailedSerializer, ClientListSerializer
from common.permissions_scopes import ClientPermissions
from common.custom import CustomPageNumberPagination
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from clients.models import Client


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.filter(
        deleted_at__isnull=True).order_by("-created_at")
    serializer_class = ClientSerializer
    pagination_class = CustomPageNumberPagination
    permission_classes = (ClientPermissions,)
    serializer_action_classes = {
        "retrieve": ClientDetailedSerializer,
    }
    queryset_actions = {
        "destroy": Client.objects.all(),
    }

    def list(self, request):
        queryset = self.get_queryset()
        queryset = filterRecords(queryset, request, table=Client)
        if request.GET.get("items_per_page") == "-1":
            return allItems(ClientListSerializer, queryset)

        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    def retrieve(self, request, pk=None):
        client = self.get_object()
        serailizer = self.get_serializer(client)
        clientData = serailizer.data
        clientServicesFormatter(clientData)
        clientFeaturesFormatter(clientData)
        return Response(clientData)

    # def update(self, request, pk=None):
    #     client = self.get_object()
    #     data = request.data
    #     if request.data.get('name'):
    #         client.name = request.data.get('name')

    #    return Response(request.data)

    def destroy(self, request, pk=None):
        return delete(self, request, Client)

    @ action(detail=False, methods=["get"])
    def all(self, request):
        return withTrashed(self, Client, order_by="-created_at")

    @action(detail=False, methods=["get"])
    def trashed(self, request):
        return trashList(self, Client)

    @action(detail=False, methods=["post"])
    def check_uniqueness(self, request):
        if request.data.get("email"):
            try:
                Client.objects.get(email=request.data.get("email"))
                return Response({"error": "email already in use"}, status=400)
            except Client.DoesNotExist:
                return Response({"success": "email is available"}, status=200)

    # for multi restore
    @ action(detail=False, methods=["put"])
    def restore(self, request, pk=None):
        return restore(self, request, Client)

    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except(KeyError, AttributeError):
            return super().get_serializer_class()

    def get_queryset(self):
        try:
            return self.queryset_actions[self.action]
        except(KeyError, AttributeError):
            return super().get_queryset()
