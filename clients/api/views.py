import queue
from backend.clients.api.serializers import ProductSerializer, ServiceSerializer
from clients.api.serializers import ClientSerializer, ClientServiceSerializer, ClientProductSerializer, ClientProduct, ClientService, FeatureSerializer, RequirementSerializer, PricePlanSerializer
from clients.models import Client, ClientService, ClientProduct, Service, Product, PricePlan, Feature, Requirement;
from rest_framework import viewsets, status


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

class ClientServiceViewSet(viewsets.ModelViewSet):
    queryset = ClientService.objects.all()
    serializer_class = ClientServiceSerializer

class ClientProductViewSet(viewsets.ModelViewSet):
    queryset = ClientProduct.objects.all()
    serializer_class = ClientProductSerializer

class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class PricePlanViewSet(viewsets.ModelViewSet):
    queryset = PricePlan.objects.all()
    serializer_class = PricePlanSerializer

class FeatureViewSet(viewsets.ModelViewSet):
    queryset = Feature.objects.all()
    serializer_class = FeatureSerializer

class RequirementViewSet(viewsets.ModelViewSet):
    queryset = Requirement.objects.all()
    serializer_class = RequirementSerializer