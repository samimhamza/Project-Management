
from clients.api.serializers import (ClientServiceSerializer, ClientFeatureSerializer,
                                     ClientFeature, ClientService, FeatureSerializer,
                                     RequirementSerializer, PricePlanSerializer)
from clients.models import (
    ClientService, ClientFeature, Service, Product, PricePlan, Feature, Requirement)
from clients.api.serializers import ProductSerializer, ServiceSerializer
from common.custom import CustomPageNumberPagination
from rest_framework.response import Response
from rest_framework import viewsets


class ClientServiceViewSet(viewsets.ModelViewSet):
    queryset = ClientService.objects.all()
    serializer_class = ClientServiceSerializer


class ClientFeatureViewSet(viewsets.ModelViewSet):
    queryset = ClientFeature.objects.all()
    serializer_class = ClientFeatureSerializer


class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.filter(
        deleted_at__isnull=True).order_by("-created_at")
    serializer_class = ServiceSerializer

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


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(
        deleted_at__isnull=True).order_by("-created_at")
    serializer_class = ProductSerializer
    pagination_class = CustomPageNumberPagination

    def list(self, request):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)


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
