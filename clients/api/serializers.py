from clients.models import ClientFeature, PricePlan, Feature, Requirement
from users.api.serializers import UserWithProfileSerializer
from rest_framework import serializers


class ClientFeatureSerializer(serializers.ModelSerializer):

    class Meta:
        model = ClientFeature
        fields = "__all__"


class FeatureCustomSerializer(serializers.ModelSerializer):
    price_plans = serializers.SerializerMethodField()

    def get_price_plans(self, feature):
        qs = PricePlan.objects.filter(feature=feature)
        serializers = PricePlanSerializer(instance=qs, many=True)
        return serializers.data

    class Meta:
        model = Feature
        fields = "__all__"


class PricePlanSerializer(serializers.ModelSerializer):

    class Meta:
        model = PricePlan
        fields = "__all__"


class PricePlanListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PricePlan
        fields = ["id", "plan_name", "plan_price"]


class FeatureListSerializer(serializers.ModelSerializer):
    price_plans = serializers.SerializerMethodField()

    def get_price_plans(self, feature):
        qs = PricePlan.objects.filter(feature=feature)
        serializers = PricePlanListSerializer(instance=qs, many=True)
        return serializers.data

    class Meta:
        model = Feature
        fields = ["id", "name", "type", "price_plans"]


class RequirementSerializer(serializers.ModelSerializer):
    created_by = UserWithProfileSerializer(read_only=True)
    updated_by = UserWithProfileSerializer(read_only=True)
    deleted_by = UserWithProfileSerializer(read_only=True)

    class Meta:
        model = Requirement
        fields = "__all__"
