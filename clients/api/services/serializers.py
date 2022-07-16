from users.api.serializers import UserWithProfileSerializer
from rest_framework import serializers
from clients.models import Service


class ServiceListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Service
        fields = ["id", "name"]


class ServiceSerializer(serializers.ModelSerializer):
    created_by = UserWithProfileSerializer(read_only=True)
    updated_by = UserWithProfileSerializer(read_only=True)
    deleted_by = UserWithProfileSerializer(read_only=True)
    parent = ServiceListSerializer(read_only=True)

    class Meta:
        model = Service
        fields = "__all__"


class ServiceCustomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ["name", "description"]


class ServiceTrashedSerializer(serializers.ModelSerializer):
    created_by = UserWithProfileSerializer(read_only=True)
    updated_by = UserWithProfileSerializer(read_only=True)
    deleted_by = UserWithProfileSerializer(read_only=True)

    class Meta:
        model = Service
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
