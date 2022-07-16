from common.actions import (clientFeaturesFormatter,
                            clientServicesFormatter, filterRecords, allItems)
from .serializers import (ClientSerializer, ClientDetailedSerializer,
                          ClientListSerializer, ClientTrashedSerializer)
from common.permissions_scopes import ClientPermissions
from rest_framework.response import Response
from rest_framework.decorators import action
from common.Repository import Repository
from clients.models import Client


class ClientViewSet(Repository):
    model = Client
    queryset = Client.objects.filter(
        deleted_at__isnull=True).order_by("-created_at")
    serializer_class = ClientSerializer
    permission_classes = (ClientPermissions,)
    serializer_action_classes = {
        "trashed": ClientTrashedSerializer,
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

    @action(detail=False, methods=["post"])
    def check_uniqueness(self, request):
        if request.data.get("email"):
            try:
                Client.objects.get(email=request.data.get("email"))
                return Response({"error": "email already in use"}, status=400)
            except Client.DoesNotExist:
                return Response({"success": "email is available"}, status=200)
