import re
from clients.actions import clientProductsFormatter, clientServicesFormatter, setProducts, setServices
from common.actions import (filterRecords, allItems, convertBase64ToImage)
from .serializers import (ClientSerializer, ClientDetailedSerializer,
                          ClientListSerializer, ClientTrashedSerializer)
from common.permissions_scopes import ClientPermissions
from rest_framework.response import Response
from rest_framework.decorators import action
from common.Repository import Repository
from clients.models import Client
from rest_framework import status
from projects.models import Country


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
        if request.GET.get("items_per_page") == "-2":
            return allItems(self.get_serializer, queryset)

        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    def retrieve(self, request, pk=None):
        client = self.get_object()
        serailizer = self.get_serializer(client)
        clientData = serailizer.data
        clientServicesFormatter(clientData)
        clientProductsFormatter(clientData)
        return Response(clientData)

    def create(self, request):
        data = request.data
        imageField = convertBase64ToImage(data["profile"])
        try:
            country = Country.objects.get(pk=data["country"])
        except Country.DoesNotExist:
            return Response({"error": "Country does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        data["created_by"] = request.user
        new_client = Client.objects.create(
            email=data["email"],
            first_name=data["first_name"],
            last_name=data["last_name"],
            phone=data["phone"],
            whatsapp=data["whatsapp"],
            profile=imageField,
            country=country,
            industry=data["industry"] if data["industry"] else "",
            company_name=data["company_name"],
            hear_about_us=data["hear_about_us"],
            lead_type=data["lead_type"],
            prefer_com_way=data["prefer_com_way"],
            # is_requirement_ready=data["is_requirement_ready"],
            # need_for_demo=data["need_for_demo"],
            # status=data["status"],
            # date=data["date"],
            created_by=data["created_by"],
            updated_by=data["created_by"],
        )
        setProducts(new_client, data)
        setServices(new_client, data)
        serializer = self.get_serializer(
            new_client, context={"request": request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        client = self.get_object()
        data = request.data
        imageField = convertBase64ToImage(data["profile"])
        if request.data.get('country'):
            try:
                country = Country.objects.get(pk=request.data["country"])
            except Country.DoesNotExist:
                return Response({"error": "Country does not exist"}, status=status.HTTP_400_BAD_REQUEST)
            client.country = country
            
        for key, value in request.data.items():
            if key != "country" and key != "products" and key != "services" and key !="profile":
                setattr(client, key, value)
        client.updated_by = request.user
        client.profile = imageField
        client.save()
        setProducts(client, data)
        setServices(client, data)

        serializer = self.get_serializer(client)
        return Response(serializer.data, status=202)

    @action(detail=False, methods=["post"])
    def check_uniqueness(self, request):
        if request.data.get("email"):
            try:
                Client.objects.get(email=request.data.get("email"))
                return Response({"error": "email already in use"}, status=400)
            except Client.DoesNotExist:
                return Response({"success": "email is available"}, status=200)
