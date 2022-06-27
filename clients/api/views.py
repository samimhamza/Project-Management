from common.actions import (withTrashed, trashList, delete, restore, clientProductsFormatter, clientServicesFormatter)
from clients.api.serializers import ClientSerializer, ClientServiceSerializer, ClientProductSerializer, ClientProduct, ClientService, FeatureSerializer, RequirementSerializer, PricePlanSerializer
from clients.models import Client, ClientService, ClientProduct, Service, Product, PricePlan, Feature, Requirement
from clients.api.serializers import ProductSerializer, ServiceSerializer, ClientDetailedSerializer
from common.permissions_scopes import ClientPermissions
from common.custom import CustomPageNumberPagination
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from clients.models import Service


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.filter(
        deleted_at__isnull=True).order_by("-created_at")
    serializer_class = ClientSerializer
    pagination_class = CustomPageNumberPagination
    permission_classes = (ClientPermissions,)
    serializer_action_classes = {
        "retrieve" : ClientDetailedSerializer,
    }
    queryset_actions = {
        "destroy": Client.objects.all(),
    }

    # def list(self, request):
    #     queryset = self.get_queryset()
    #     page = self.paginate_queryset(queryset)
    #     serializer = self.get_serializer(page, many=True)
    #     for client in serializer.data:
    #         clientServicesFormatter(client)
    #         clientProductsFormatter(client)
    #     return self.get_paginated_response(serializer.data)

    def retrieve(self, request, pk=None):
        client = self.get_object()
        serailizer = self.get_serializer(client)
        clientData = serailizer.data
        clientServicesFormatter(clientData)
        clientProductsFormatter(clientData)
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

    @ action(detail=False, methods=["get"])
    def trashed(self, request):
        return trashList(self, Client)

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
        except(KeyError,AttributeError):
            return super().get_queryset()
    

class ClientServiceViewSet(viewsets.ModelViewSet):
    queryset = ClientService.objects.all()
    serializer_class = ClientServiceSerializer


class ClientProductViewSet(viewsets.ModelViewSet):
    queryset = ClientProduct.objects.all()
    serializer_class = ClientProductSerializer


class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.filter(
        deleted_at__isnull=True).order_by("-created_at")
    serializer_class = ServiceSerializer

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(
        deleted_at__isnull=True).order_by("-created_at")
    serializer_class = ProductSerializer
    pagination_class = CustomPageNumberPagination

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class PricePlanViewSet(viewsets.ModelViewSet):
    queryset = PricePlan.objects.filter(
        deleted_at__isnull=True).order_by("-created_at")
    serializer_class = PricePlanSerializer

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class FeatureViewSet(viewsets.ModelViewSet):
    queryset = Feature.objects.filter(
        deleted_at__isnull=True).order_by("-created_at")
    serializer_class = FeatureSerializer

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class RequirementViewSet(viewsets.ModelViewSet):
    queryset = Requirement.objects.filter(
        deleted_at__isnull=True).order_by("-created_at")
    serializer_class = RequirementSerializer

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
