from users.api.serializers import UserWithProfileSerializer
from rest_framework import serializers
from projects.models import (
    Country,
    Location,
    FocalPoint,
    Income,
    Payment,
    Project,
    Attachment,
    State
)


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = "__all__"


class CountryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ["id", "name"]


class StateListSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = ["id", "name"]


class StateSerializer(serializers.ModelSerializer):
    country = CountryListSerializer(read_only=True)

    class Meta:
        model = State
        fields = ["id", "name", "state_code",
                  "latitude", "longitude", "country"]


class LocationSerializer(serializers.ModelSerializer):
    state = StateSerializer(read_only=True)

    class Meta:
        model = Location
        fields = [
            "id",
            "address_line_one",
            "address_line_two",
            "city",
            "state",
        ]


class FocalPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = FocalPoint
        fields = "__all__"


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"


class IncomeSerializer(serializers.ModelSerializer):
    payments = serializers.SerializerMethodField()

    def get_payments(self, income):
        qs = Payment.objects.filter(
            deleted_at__isnull=True, income=income)
        serializer = PaymentSerializer(instance=qs, many=True)
        return serializer.data

    class Meta:
        model = Income
        fields = "__all__"


class ProjectLessListSerializer(serializers.ModelSerializer):
    company_location = LocationSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = [
            "id",
            "name",
            "description",
            "p_start_date",
            "p_end_date",
            "a_start_date",
            "a_end_date",
            "status",
            "progress",
            "priority",
            "company_name",
            "company_email",
            "company_location",
        ]


class ProjectNameListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = [
            "id",
            "name",
        ]


class AttachmentSerializer(serializers.ModelSerializer):
    uploaded_by = UserWithProfileSerializer()

    class Meta:
        model = Attachment
        fields = ["id", "name", "attachment",
                  "size", "description", "uploaded_by", "created_at"]


class FocalPointTrashedSerializer(serializers.ModelSerializer):
    created_by = UserWithProfileSerializer(read_only=True)
    updated_by = UserWithProfileSerializer(read_only=True)
    deleted_by = UserWithProfileSerializer(read_only=True)
    name = serializers.SerializerMethodField()

    def get_name(self, obj):
        return '{} {}'.format(obj.contact_name, obj.contact_last_name)

    class Meta:
        model = FocalPoint
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


class IncomeTrashedSerializer(serializers.ModelSerializer):
    created_by = UserWithProfileSerializer(read_only=True)
    updated_by = UserWithProfileSerializer(read_only=True)
    deleted_by = UserWithProfileSerializer(read_only=True)
    name = serializers.CharField(source="title")

    class Meta:
        model = FocalPoint
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


class PaymentTrashedSerializer(serializers.ModelSerializer):
    created_by = UserWithProfileSerializer(read_only=True)
    updated_by = UserWithProfileSerializer(read_only=True)
    deleted_by = UserWithProfileSerializer(read_only=True)
    name = serializers.CharField(source="source")

    class Meta:
        model = FocalPoint
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
