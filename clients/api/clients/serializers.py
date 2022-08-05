from clients.models import (Client, ClientService, ClientFeature, Requirement)
from clients.api.services.serializers import ServiceCustomSerializer
from clients.api.products.serializers import LessFieldsFeatureSerializer
from users.api.serializers import UserWithProfileSerializer
from projects.api.serializers import CountryListSerializer
from clients.api.serializers import RequirementSerializer
from rest_framework import serializers


class ClientServiceListSerializer(serializers.ModelSerializer):
    service = ServiceCustomSerializer()

    class Meta:
        model = ClientService
        fields = ["id", "service", "details"]


class ClientFeatureCustomSerializer(serializers.ModelSerializer):
    feature = LessFieldsFeatureSerializer()

    class Meta:
        model = ClientFeature
        exclude = ['id', 'client']
        # fields = ["plan","on_request_price","on_request_date","purchased_price","purchased_date","end_date","feature"]


class ClientListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Client
        fields = ["id", "first_name", "last_name", "profile"]


class ClientSerializer(serializers.ModelSerializer):
    created_by = UserWithProfileSerializer(read_only=True)
    updated_by = UserWithProfileSerializer(read_only=True)
    deleted_by = UserWithProfileSerializer(read_only=True)
    country = CountryListSerializer()

    class Meta:
        model = Client
        fields = "__all__"


class ClientDetailedSerializer(serializers.ModelSerializer):
    services = serializers.SerializerMethodField()
    features = serializers.SerializerMethodField()
    requirement = RequirementSerializer()
    created_by = UserWithProfileSerializer(read_only=True)
    updated_by = UserWithProfileSerializer(read_only=True)
    deleted_by = UserWithProfileSerializer(read_only=True)

    def get_services(self, client):
        qs = ClientService.objects.filter(client=client)
        serializer = ClientServiceListSerializer(instance=qs, many=True)
        return serializer.data

    def get_features(self, client):
        qs = ClientFeature.objects.filter(client=client)
        serializers = ClientFeatureCustomSerializer(instance=qs, many=True)
        return serializers.data

    class Meta:
        model = Client
        fields = ["id", "first_name", "last_name", "phone", "whatsapp", "email", "profile", "country", "company_name",
                  "industry", "services", "features", "hear_about_us", "lead_type", "prefer_com_way", "is_requirement_ready",
                  "status", "date", "requirement", "created_by", "updated_by", "created_at", "updated_at", "deleted_by", "deleted_at"]


class ClientServiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = ClientService
        fields = "__all__"


class ClientTrashedSerializer(serializers.ModelSerializer):
    created_by = UserWithProfileSerializer(read_only=True)
    updated_by = UserWithProfileSerializer(read_only=True)
    deleted_by = UserWithProfileSerializer(read_only=True)
    name = serializers.SerializerMethodField()

    def get_name(self, obj):
        return '{} {}'.format(obj.first_name, obj.last_name)

    class Meta:
        model = Client
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
