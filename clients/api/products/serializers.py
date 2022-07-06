from users.api.serializers import UserWithProfileSerializer
from clients.api.serializers import FeatureCustomSerializer
from clients.models import Feature, Product
from rest_framework import serializers


class ProductListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ["id", "name", "deleted_by", "photo"]


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


class FeatureSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    created_by = UserWithProfileSerializer(read_only=True)
    updated_by = UserWithProfileSerializer(read_only=True)
    deleted_by = UserWithProfileSerializer(read_only=True)

    class Meta:
        model = Feature
        fields = "__all__"
