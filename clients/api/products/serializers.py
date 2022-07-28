from users.api.serializers import UserWithProfileSerializer
from clients.api.serializers import FeatureCustomSerializer, FeatureListSerializer
from clients.models import Feature, Product
from rest_framework import serializers


class ProductListSerializer(serializers.ModelSerializer):
    features = serializers.SerializerMethodField()

    def get_features(self, product):
        qs = Feature.objects.filter(product=product)
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
        qs = Feature.objects.filter(product=product)
        serializers = FeatureCustomSerializer(instance=qs, many=True)
        return serializers.data

    class Meta:
        model = Product
        fields = "__all__"


class LessFieldsProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ["id", "name", "developed_by", "details", "photo"]


class FeatureSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = Feature
        fields = "__all__"


class LessFieldsFeatureSerializer(serializers.ModelSerializer):
    product = LessFieldsProductSerializer()

    class Meta:
        model = Feature
        fields = ["id", "name", "description", "type", "product"]


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
