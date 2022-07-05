from clients.api.serializers import (
    ClientServiceListSerializer, ClientFeatureCustomSerializer, RequirementSerializer)
from clients.models import (Client, ClientService, ClientFeature, Requirement)
from users.api.serializers import UserWithProfileSerializer
from rest_framework import serializers
from projects.api.serializers import CountryListSerializer


class ClientSerializer(serializers.ModelSerializer):
    created_by = UserWithProfileSerializer(read_only=True)
    updated_by = UserWithProfileSerializer(read_only=True)
    country = CountryListSerializer()

    class Meta:
        model = Client
        fields = "__all__"


class ClientDetailedSerializer(serializers.ModelSerializer):
    services = serializers.SerializerMethodField()
    features = serializers.SerializerMethodField()
    requirement = serializers.SerializerMethodField()
    created_by = UserWithProfileSerializer(read_only=True)
    updated_by = UserWithProfileSerializer(read_only=True)

    def get_services(self, client):
        qs = ClientService.objects.filter(client=client)
        serializer = ClientServiceListSerializer(instance=qs, many=True)
        return serializer.data

    def get_features(self, client):
        qs = ClientFeature.objects.filter(client=client)
        serializers = ClientFeatureCustomSerializer(instance=qs, many=True)
        return serializers.data

    def get_requirement(self, client):
        qs = Requirement.objects.get(client=client)
        serializers = RequirementSerializer(instance=qs)
        return serializers.data

    class Meta:
        model = Client
        fields = "__all__"
