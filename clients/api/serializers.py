from dataclasses import field
from clients.models import Client, ClientService, ClientProduct, Service, Product, PricePlan, Feature, Requirement;
from rest_framework import serializers

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = "__all__"

class ClientServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientService
        fields = "__all__"

class ClientProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientProduct
        fields = "__all__"

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
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