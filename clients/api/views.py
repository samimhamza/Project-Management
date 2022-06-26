from clients.api.serializers import ClientSerializer, ClientServiceSerializer, ClientProductSerializer, ClientProduct, ClientService, FeatureSerializer, RequirementSerializer, PricePlanSerializer
from clients.models import Client, ClientService, ClientProduct, Service, Product, PricePlan, Feature, Requirement;
from clients.api.serializers import ProductSerializer, ServiceSerializer
from common.custom import CustomPageNumberPagination
from rest_framework import viewsets, status
from rest_framework.response import Response

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.filter(
    deleted_at__isnull=True).order_by("-created_at")
    pagination_class = CustomPageNumberPagination
    serializer_class = ClientSerializer

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