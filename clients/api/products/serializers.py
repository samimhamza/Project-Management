from users.api.serializers import UserWithProfileSerializer
from clients.api.serializers import FeatureCustomSerializer, FeatureListSerializer
from clients.models import Feature, Product
from rest_framework import serializers


class ProductListSerializer(serializers.ModelSerializer):
    features = serializers.SerializerMethodField()

    def get_features(self, product):
        qs = Feature.objects.filter(deleted_at__isnull=True, product=product)
        serializers = FeatureListSerializer(instance=qs, many=True)
        return serializers.data

    class Meta:
        model = Product
        fields = ["id", "name", "photo", "features"]


class ProductSerializer(serializers.ModelSerializer):
    features = serializers.SerializerMethodField()
    created_by = UserWithProfileSerializer(read_only=True)
    updated_by = UserWithProfileSerializer(read_only=True)
    deleted_by = UserWithProfileSerializer(read_only=True)

    def get_features(self, product):
        qs = Feature.objects.filter(deleted_at__isnull=True, product=product)
        serializers = FeatureCustomSerializer(instance=qs, many=True)
        return serializers.data

    class Meta:
        model = Product
        fields = "__all__"


class FeatureSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    created_by = UserWithProfileSerializer(read_only=True)
    updated_by = UserWithProfileSerializer(read_only=True)
    deleted_by = UserWithProfileSerializer(read_only=True)

    class Meta:
        model = Feature
        fields = "__all__"


class ProductTrashedSerializer(serializers.ModelSerializer):
    created_by = UserWithProfileSerializer(read_only=True)
    updated_by = UserWithProfileSerializer(read_only=True)
    deleted_by = UserWithProfileSerializer(read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "created_at",
            "updated_at",
            "deleted_at",
            "created_by",
            "updated_by",
            "deleted_by"
        ]
