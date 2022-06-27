from dataclasses import field
from clients.models import (Client, ClientService, ClientProduct,
                            Service, Product, PricePlan, Feature, Requirement)
from rest_framework import serializers


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = "__all__"


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = "__all__"


class ClientDetailedSerializer(serializers.ModelSerializer):
    services = serializers.SerializerMethodField()
    features = serializers.SerializerMethodField()
    requirement = serializers.SerializerMethodField()

    def get_services(self, client):
        qs = ClientService.objects.filter(client=client)
        serializer = ClientServiceListSerializer(instance=qs, many=True)
        return serializer.data

    def get_features(self, client):
        qs = ClientProduct.objects.filter(client=client)
        serializers = ClientProductCustomSerializer(instance=qs, many=True)
        return serializers.data

    def get_requirement(self, client):
        qs = Requirement.objects.get(client=client)
        serializers = RequirementSerializer(instance=qs)
        return serializers.data
    class Meta:
        model = Client
        fields = "__all__"



class ServiceCustomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ["name","description"]

class ClientServiceListSerializer(serializers.ModelSerializer):
    service = ServiceCustomSerializer()

    class Meta:
        model = ClientService
        fields = ["id","service", "details"]
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


class FeatureSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    class Meta:
        model = Feature
        fields = "__all__"
class ClientProductCustomSerializer(serializers.ModelSerializer):
    feature = FeatureSerializer()
    class Meta:
        model = ClientProduct
        exclude = ('id','client', )
        # fields = ["plan","on_request_price","on_request_date","purchased_price","purchased_date","end_date","feature"]



class PricePlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = PricePlan
        fields = "__all__"


class RequirementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Requirement
        fields = "__all__"
