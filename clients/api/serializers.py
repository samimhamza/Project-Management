from clients.models import (Client, ClientService, ClientProduct,
                            Service, Product, PricePlan, Feature, Requirement)
from rest_framework import serializers


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = "__all__"


class ClientSerializer(serializers.ModelSerializer):
    services = serializers.SerializerMethodField()

    def get_services(self, client):
        qs = ClientService.objects.filter(client=client)
        serializer = ClientServiceListSerializer(instance=qs, many=True)
        return serializer.data

    class Meta:
        model = Client
        fields = "__all__"


class ClientServiceListSerializer(serializers.ModelSerializer):
    service = ServiceSerializer()

    class Meta:
        model = ClientService
        fields = ["service", "details"]


class ClientServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientService
        fields = "__all__"


class ClientProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientProduct
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class PricePlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = PricePlan
        fields = "__all__"


class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = "__all__"


class RequirementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Requirement
        fields = "__all__"
