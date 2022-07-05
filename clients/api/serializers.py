from clients.models import (
    ClientService, ClientFeature, Service, Product, PricePlan, Feature, Requirement)
from rest_framework import serializers


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = "__all__"


class ServiceCustomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ["name", "description"]


class ClientServiceListSerializer(serializers.ModelSerializer):
    service = ServiceCustomSerializer()

    class Meta:
        model = ClientService
        fields = ["id", "service", "details"]


class ClientServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientService
        fields = "__all__"


class ClientFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientFeature
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    features = serializers.SerializerMethodField()

    def get_features(self, product):
        qs = Feature.objects.filter(product=product)
        serializers = FeatureCustomSerializer(instance=qs, many=True)
        return serializers.data

    class Meta:
        model = Product
        fields = "__all__"


class FeatureSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = Feature
        fields = "__all__"


class FeatureCustomSerializer(serializers.ModelSerializer):
    price_plan = serializers.SerializerMethodField()

    def get_price_plan(self, feature):
        qs = PricePlan.objects.filter(feature=feature)
        serializers = PricePlanSerializer(instance=qs, many=True)
        return serializers.data

    class Meta:
        model = Feature
        fields = "__all__"


class ClientFeatureCustomSerializer(serializers.ModelSerializer):
    feature = FeatureSerializer()

    class Meta:
        model = ClientFeature
        exclude = ('id', 'client', )
        # fields = ["plan","on_request_price","on_request_date","purchased_price","purchased_date","end_date","feature"]


class PricePlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = PricePlan
        fields = "__all__"


class RequirementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Requirement
        fields = "__all__"
