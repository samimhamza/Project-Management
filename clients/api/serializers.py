from dataclasses import field
from clients.models import Client, ClientService, ClientProduct, Service, Product, PricePlan, Feature, Requirement;
from rest_framework import serializers

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        field = "__all__"

class ClientServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientService
        field = "__all__"

class ClientProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientProduct
        field = "__all__"

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        field = "__all__"

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        field = "__all__"

class PricePlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = PricePlan
        field = "__all__"

class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        field = "__all__"

class RequirementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Requirement
        field = "__all__"